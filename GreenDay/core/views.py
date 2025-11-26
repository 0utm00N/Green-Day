# ============================================================
# 📦 IMPORTS
# ============================================================

# --- Librerías externas ---
import logging
import paypalrestsdk
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType


# --- Django ---
from django.db import IntegrityError
from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# --- Módulos internos ---
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import PerfilForm, RegistroForm
from .firebase_utils import (
    guardar_itemcarrito_firebase,
    sincronizar_carrito_firebase,
    guardar_pedido_firebase,
    guardar_cliente_firebase
)

# Logger
logger = logging.getLogger(__name__)

# ============================================================
# 🏠 HOME
# ============================================================

def home(request):
    productos_destacados = Producto.objects.all()[:6]
    return render(request, "core/home.html", {"productos": productos_destacados})


# ============================================================
# 🛍️ CATÁLOGO
# ============================================================

def catalogo(request):
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'core/catalogo.html', {'productos': productos})



def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    tips_list = producto.tips.splitlines() if producto.tips else []
    
    return render(request, 'core/producto_detalle.html', {
        'producto': producto,
        'tips_list': tips_list,
    })

# ============================================================
# 🛒 CARRITO
# ============================================================

@require_POST
@login_required
def agregar_al_carrito(request, producto_id):
    """Agrega productos al carrito, validando cantidad y stock disponible."""
    try:
        if not hasattr(request.user, 'cliente'):
            return JsonResponse({'success': False, 'error': 'El usuario no tiene cliente asociado.'})

        cliente = request.user.cliente
        carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
        producto = get_object_or_404(Producto, id=producto_id)

        # Obtener cantidad desde el request
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except ValueError:
            cantidad = 1
        if cantidad < 1:
            cantidad = 1

        # Validar stock
        if cantidad > producto.stock:
            return JsonResponse({'success': False, 'error': 'Cantidad solicitada supera el stock disponible.'})

        # Crear o actualizar el ítem
        item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()
        if item:
            if item.cantidad + cantidad > producto.stock:
                return JsonResponse({'success': False, 'error': 'No hay suficiente stock disponible.'})
            item.cantidad += cantidad
        else:
            item = ItemCarrito(carrito=carrito, producto=producto, cantidad=cantidad)
        item.save()

        # Total de unidades
        total_items = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0

        return JsonResponse({
            'success': True,
            'count': total_items,
            'producto': producto.nombre,
            'cantidad': item.cantidad
        })

    except Exception as e:
        logger.exception("Error al agregar producto al carrito")
        return JsonResponse({'success': False, 'error': 'Ocurrió un error interno en el servidor.'})


@login_required
def ver_carrito(request):
    """Renderiza el carrito del usuario con todos los productos agregados."""
    cliente = request.user.cliente
    carrito, _ = Carrito.objects.get_or_create(cliente=cliente)

    productos = []
    total = 0
    for item in carrito.items.all():
        subtotal = item.producto.precio * item.cantidad
        productos.append({
            'id': item.producto.id,
            'nombre': item.producto.nombre,
            'cantidad': item.cantidad,
            'subtotal': subtotal,
            'imagen': item.producto.imagen
        })
        total += subtotal

    return render(request, 'core/carrito.html', {'productos': productos, 'total': total})

@login_required
def eliminar_del_carrito(request):
    if request.method == "POST":
        try:
            producto_id = request.POST.get("producto_id")

            cliente = request.user.cliente
            carrito = Carrito.objects.get(cliente=cliente)

            item = ItemCarrito.objects.filter(carrito=carrito, producto_id=producto_id).first()

            if not item:
                return JsonResponse({"success": False, "error": "Producto no encontrado en el carrito"})

            item.delete()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})


@login_required
def contador_carrito(request):
    """Devuelve la cantidad total de unidades en el carrito."""
    try:
        carrito = Carrito.objects.get(cliente=request.user.cliente)
        count = sum(item.cantidad for item in carrito.items.all())
    except Carrito.DoesNotExist:
        count = 0

    return JsonResponse({'count': count})

@login_required
def opcion_despacho(request):
    return render(request, "core/despacho.html")

@login_required
def opcion_retiro(request):
    return render(request, "core/retiro.html")




# ============================================================
# 📦 PEDIDOS
# ============================================================

def descontar_stock(pedido):
    for detalle in pedido.detalles.all():
        producto = detalle.producto
        producto.stock -= detalle.cantidad

        if producto.stock <= 0:
            producto.stock = 0
            producto.disponible = False  # 🔥 Desactivar producto

        producto.save()


@login_required
def finalizar_pedido(request):
    if request.method != "POST":
        return redirect("ver_carrito")

    cliente = request.user.cliente

    metodo_pago = request.POST.get("metodo_pago")          # transbank / paypal
    metodo_entrega = request.POST.get("metodo_entrega")    # despacho / retiro
    direccion = request.POST.get("direccion_final")

    carrito = Carrito.objects.get(cliente=cliente)

    # Calcular monto total
    total = sum(item.producto.precio * item.cantidad for item in carrito.items.all())

    # 1) Crear un pedido PENDIENTE (todavía no sabemos el estado)
    pedido = Pedido.objects.create(
        cliente=cliente,
        total=total,
        metodo_pago=metodo_pago,
        tipo_entrega="Despacho" if metodo_entrega == "despacho" else "Retiro",
        direccion_envio=direccion if metodo_entrega == "despacho" else None,
        estado="EP"  # Esperando Pago
    )

    # 2) Guardar detalles del pedido
    for item in carrito.items.all():
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )

    # ============================================
    # 3) REDIRECCIÓN SEGÚN MÉTODO DE PAGO ELEGIDO
    # ============================================

    if metodo_pago == "transbank":
        return iniciar_pago_transbank(request, pedido)

    elif metodo_pago == "paypal":
        return iniciar_pago_paypal(request, pedido)

    else:
        return render(request, "core/pago_fallido.html", {
            "error": "Método de pago no válido"
        })



@login_required
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user.cliente).order_by('-fecha')
    return render(request, 'core/historial_pedidos.html', {'pedidos': pedidos})


@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user.cliente)
    detalles = pedido.detalles.all()
    return render(request, 'core/detalle_pedido.html', {'pedido': pedido, 'detalles': detalles})


def pedido_exitoso(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    return render(request, 'core/pedido_exitoso.html', {'pedido': pedido})


# ============================================================
# 👤 PERFIL
# ============================================================

@login_required
def ver_perfil(request):
    cliente = request.user.cliente
    if request.method == "POST":
        form = PerfilForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente ✅")
            return redirect('ver_perfil')
    else:
        form = PerfilForm(instance=cliente)
    return render(request, 'core/perfil.html', {'form': form})


# ============================================================
# 🔐 LOGIN / LOGOUT
# ============================================================

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except Exception as e:
                print("ERROR REAL:", e)
                raise   # <-- Que Django muestre el error REAL
            login(request, user)
            return redirect('catalogo')
    else:
        form = RegistroForm()

    return render(request, 'core/registro.html', {'form': form})





def logout_view(request):
    logout(request)
    return redirect('catalogo')


# ============================================================
# 💳 PAGOS SIMULADOS
# ============================================================

def iniciar_pago_transbank(request, pedido):

    options = WebpayOptions(
    commerce_code=settings.TRANSBANK_COMMERCE_CODE,
    api_key=settings.TRANSBANK_API_KEY,
    integration_type=IntegrationType.TEST
    )
    tx = Transaction(options)



    response = tx.create(
        buy_order=str(pedido.id),
        session_id=str(request.user.id),
        amount=float(pedido.total),
        return_url=request.build_absolute_uri("/transbank/confirmar/")
    )

    pedido.transbank_token = response["token"]
    pedido.save()

    return redirect(response["url"] + "?token_ws=" + response["token"])

@login_required
def confirmar_transbank(request):
    token = request.GET.get("token_ws")

    if not token:
        return redirect("catalogo")

    options = WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
        integration_type=IntegrationType.TEST  # o IntegrationType.INTEGRATION si estás usando "integration"
    )

    tx = Transaction(options)

    try:
        result = tx.commit(token)
    except Exception as e:
        print("Error al confirmar pago:", e)
        messages.error(request, "Error al confirmar el pago.")
        return redirect("catalogo")

    if result["status"] == "AUTHORIZED":
        # Recuperar pedido por buy_order
        pedido = Pedido.objects.get(id=result["buy_order"])
        pedido.estado = "pagado"
        pedido.save()

        descontar_stock(pedido)

        # Vaciar carrito
        ItemCarrito.objects.filter(carrito__cliente=request.user.cliente).delete()


        return render(request, "core/pedido_exitoso.html", {"pedido": pedido})

    else:
        messages.error(request, "Pago rechazado.")
        return redirect("catalogo")


def iniciar_pago_paypal(request, pedido):
    # Configurar credenciales PayPal
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,  # sandbox / live
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    # Crear orden PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",

        "payer": {
            "payment_method": "paypal"
        },

        "redirect_urls": {
            "return_url": request.build_absolute_uri(f"/paypal/confirmar/?pedido={pedido.id}"),
            "cancel_url": request.build_absolute_uri("/paypal/cancelado/")
        },

        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"Pedido #{pedido.id}",
                    "sku": str(pedido.id),
                    "price": str(pedido.total),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(pedido.total),
                "currency": "USD"
            },
            "description": f"Compra en GreenDay. Pedido #{pedido.id}",
        }]
    })

    # Crear pago en PayPal
    if payment.create():
        print("PayPal Payment Created")

        # Guardamos el order_id en el pedido
        pedido.paypal_order_id = payment.id
        pedido.save()

        # Buscar link de aprobación
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return redirect(approval_url)

        return render(request, "core/pago_fallido.html", {
            "error": "PayPal no devolvió la URL de aprobación."
        })

    else:
        print(payment.error)
        return render(request, "core/pago_fallido.html", {
            "error": "No se pudo crear la transacción con PayPal."
        })

@login_required
def confirmar_paypal(request):
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")
    pedido_id = request.GET.get("pedido")

    pedido = Pedido.objects.get(id=pedido_id)

    # Recuperamos el pago enviado por PayPal
    payment = paypalrestsdk.Payment.find(payment_id)

    # Ejecutar el pago
    if payment.execute({"payer_id": payer_id}):

        pedido.estado = "PA"  # Pagado

        # Guardar datos importantes
        pedido.paypal_payer_id = payer_id
        pedido.paypal_status = payment.state
        pedido.paypal_email = payment.payer["payer_info"]["email"]
        pedido.paypal_response = payment.to_dict()
        pedido.save()


        descontar_stock(pedido)


        # Vaciar carrito
        Carrito.objects.filter(cliente=request.user.cliente).delete()

        return render(request, "core/pedido_exitoso.html", {
            "pedido": pedido,
            "response": payment.to_dict()
        })

    else:
        pedido.estado = "R"
        pedido.save()

        return render(request, "core/pago_fallido.html", {
            "pedido": pedido,
            "response": payment.error
        })

def paypal_cancelado(request):
    return render(request, "core/pago_fallido.html", {
        "error": "El pago fue cancelado por el usuario."
    })
