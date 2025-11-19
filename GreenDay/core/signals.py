from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cliente, Carrito, ItemCarrito, Pedido, DetallePedido
from .firebase_utils import guardar_cliente_firebase, sincronizar_carrito_firebase, guardar_pedido_firebase

# 🔹 Crear cliente automáticamente al registrar un usuario y sincronizarlo
@receiver(post_save, sender=User)
def crear_cliente(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'cliente'):
        cliente = Cliente.objects.create(
            user=instance,
            nombre=instance.username,
            apellido="",
            direccion="Pendiente",
            telefono="Pendiente"
        )
        # Crear carrito vacío para el cliente
        Carrito.objects.create(cliente=cliente)
        # Guardar en Firebase
        guardar_cliente_firebase(cliente)

# 🔹 Sincronizar el carrito cuando se agregan o modifican ítems
@receiver(post_save, sender=ItemCarrito)
def actualizar_item_carrito(sender, instance, created, **kwargs):
    if instance.carrito:
        sincronizar_carrito_firebase(instance.carrito)

# 🔹 Guardar pedido en Firebase al crearlo
@receiver(post_save, sender=Pedido)
def guardar_pedido(sender, instance, created, **kwargs):
    if created:
        guardar_pedido_firebase(instance)

