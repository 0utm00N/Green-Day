from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cliente, Carrito, ItemCarrito, Pedido
from .firebase_utils import (
    guardar_cliente_firebase,
    sincronizar_carrito_firebase,
    guardar_pedido_firebase
)

# ===========================================================
#  SIGNAL 1 → Sincronizar Cliente a Firebase si cambia
#  (YA NO CREA Cliente automáticamente)
# ===========================================================

@receiver(post_save, sender=Cliente)
def sincronizar_cliente(sender, instance, created, **kwargs):
    """
    Cuando se crea o actualiza un Cliente, enviamos sus datos a Firebase.
    Esto evita crear clientes duplicados y permite que tu formulario tenga el control.
    """
    guardar_cliente_firebase(instance)


# ===========================================================
#  SIGNAL 2 → Sync del carrito cuando se actualiza un ítem
# ===========================================================

@receiver(post_save, sender=ItemCarrito)
def actualizar_item_carrito(sender, instance, created, **kwargs):
    """
    Cada vez que un Item del carrito se crea o modifica,
    sincronizamos todo el carrito a Firebase.
    """
    if instance.carrito:
        sincronizar_carrito_firebase(instance.carrito)


# ===========================================================
#  SIGNAL 3 → Guardar pedidos en Firebase al crearse
# ===========================================================

@receiver(post_save, sender=Pedido)
def guardar_pedido(sender, instance, created, **kwargs):
    """
    Cuando un pedido se genera, lo enviamos a Firebase.
    """
    if created:
        guardar_pedido_firebase(instance)
