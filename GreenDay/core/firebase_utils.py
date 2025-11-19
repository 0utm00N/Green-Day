import firebase_admin
from firebase_admin import credentials, firestore
from .models import Carrito, ItemCarrito, Pedido, DetallePedido, Cliente

# 🔹 Inicializar Firebase solo una vez
cred = credentials.Certificate("firebase/greendaydb-c65e3-firebase-adminsdk-fbsvc-77c97acf38.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


# 🔹 Guardar un item del carrito en Firestore
def guardar_itemcarrito_firebase(item: ItemCarrito):
    doc_ref = db.collection("carritos").document(str(item.carrito.id)) \
                 .collection("items").document(str(item.id))
    doc_ref.set({
        "producto": item.producto.nombre,
        "cantidad": item.cantidad,
        "precio_unitario": float(item.producto.precio),
        "subtotal": float(item.subtotal)
    })


# 🔹 Guardar todo el carrito
def sincronizar_carrito_firebase(carrito: Carrito):
    for item in carrito.items.all():
        guardar_itemcarrito_firebase(item)


# 🔹 Guardar un pedido
def guardar_pedido_firebase(pedido: Pedido):
    doc_ref = db.collection("pedidos").document(str(pedido.id))
    doc_ref.set({
        "cliente": pedido.cliente.user.username,
        "total": float(pedido.total),
        "estado": pedido.estado,
        "fecha": pedido.fecha.isoformat(),
        "detalles": [
            {
                "producto": detalle.producto.nombre,
                "cantidad": detalle.cantidad,
                "precio_unitario": float(detalle.precio_unitario),
                "subtotal": float(detalle.subtotal)
            } for detalle in pedido.detalles.all()
        ]
    })


# 🔹 Guardar un cliente
def guardar_cliente_firebase(cliente: Cliente):
    doc_ref = db.collection("clientes").document(str(cliente.id))
    doc_ref.set({
        "username": cliente.user.username,
        "nombre": cliente.nombre,
        "apellido": cliente.apellido,
        "direccion": cliente.direccion,
        "telefono": cliente.telefono
    })
