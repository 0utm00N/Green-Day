import paypalrestsdk
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from django.http import JsonResponse
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import PerfilForm
from django.contrib import messages
from .firebase_utils import (
    guardar_itemcarrito_firebase,
    sincronizar_carrito_firebase,
    guardar_pedido_firebase,
    guardar_cliente_firebase
)

# Create your views here.

# -----------------------------
# Catálogo
# -----------------------------


def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'core/catalogo.html', {'productos': productos})

# -----------------------------
# Carrito
# -----------------------------

@login_required
def agregar_al_carrito(request, producto_id):
    if not request.user.is_authenticated:
        return redirect('login')

    cliente = request.user.cliente
    carrito, created = Carrito.objects.get_or_create(cliente=cliente)

    producto = get_object_or_404(Producto, id=producto_id)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    if not created:
        item.cantidad += 1
        item.save()
    
    messages.success(request, f"'{producto.nombre}' se ha agregado al carrito.")
    
    # Volver a la página anterior
    return redirect(request.META.get('HTTP_REFERER', 'catalogo'))

@login_required
def ver_carrito(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        # Crear cliente si no existe
        cliente = Cliente.objects.create(user=request.user, nombre=request.user.username, apellido="Pendiente")

    # Obtener o crear carrito
    carrito, created = Carrito.objects.get_or_create(cliente=cliente)

    productos = []
    total = 0

    for item in carrito.items.all():  # Asumiendo que tu modelo Carrito tiene items ManyToMany a productos
        subtotal = item.producto.precio * item.cantidad
        productos.append({
            'id': item.producto.id,
            'nombre': item.producto.nombre,
            'cantidad': item.cantidad,
            'subtotal': subtotal,
            'imagen': item.producto.imagen
        })
        total += subtotal

    context = {
        'productos': productos,
        'total': total
    }

    return render(request, 'core/carrito.html', context)


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('ver_carrito')


# -----------------------------
# Pedidos
# -----------------------------

@login_required
def finalizar_pedido(request):
    cliente = request.user.cliente

    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        carrito = Carrito.objects.filter(cliente=cliente).first()

        if not carrito or not carrito.items.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('ver_carrito')

        # Crear pedido
        pedido = Pedido.objects.create(cliente=cliente)
        total = 0

        for item in carrito.items.all():
            DetallePedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
            total += item.producto.precio * item.cantidad

        pedido.total = total
        pedido.save()

        # Vaciar carrito
        carrito.items.all().delete()

        # Redirigir según el método de pago seleccionado
        if metodo_pago == 'transbank':
            return redirect('pago_transbank', pedido_id=pedido.id)
        elif metodo_pago == 'paypal':
            return redirect('pago_paypal', pedido_id=pedido.id)
        else:
            messages.error(request, "Método de pago no válido.")
            return redirect('ver_carrito')

    return redirect('ver_carrito')


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

# -----------------------------
# Perfil
# -----------------------------

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

def logout_view(request):
    logout(request)
    return redirect('catalogo')

# --- PAGO SIMULADO TRANSBANK ---
def pago_transbank(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    confirmacion_url = f"/api/pago/transbank/confirm/?pedido_id={pedido.id}"
    return render(request, "core/redirigir_pago.html", {
        "pedido": pedido,
        "pedido_id": pedido.id,
        "url_confirmacion": confirmacion_url,
        "metodo": "Transbank"
    })


# --- PAGO SIMULADO PAYPAL ---
def pago_paypal(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    confirmacion_url = f"/api/pago/paypal/confirm/?pedido_id={pedido.id}"
    return render(request, "core/redirigir_pago.html", {
        "pedido": pedido,
        "pedido_id": pedido.id,
        "url_confirmacion": confirmacion_url,
        "metodo": "PayPal"
    })


# --- CONFIRMACIÓN DE TRANSBANK ---
def confirmar_pago_transbank(request):
    pedido_id = request.GET.get("pedido_id")
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = "C"  # Completado
    pedido.save()
    return render(request, "core/pedido_exitoso.html", {"pedido": pedido, "metodo": "Transbank"})


# --- CONFIRMACIÓN DE PAYPAL ---
def confirmar_pago_paypal(request):
    pedido_id = request.GET.get("pedido_id")
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = "C"  # Completado
    pedido.save()
    return render(request, "core/pedido_exitoso.html", {"pedido": pedido, "metodo": "PayPal"})