from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# =========================
# MODELOS PRINCIPALES
# =========================

class Invernadero(models.Model):
    """Representa el origen de los productos (vivero o productor)."""
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Plantas o artículos disponibles para la venta."""
    nombre = models.CharField(max_length=100)
    nombre_cientifico = models.CharField(max_length=150, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    # Relaciones
    invernadero = models.ForeignKey('Invernadero', on_delete=models.CASCADE, related_name='productos')

    # Descripciones
    descripcion_corta = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    cuidados = models.TextField(blank=True, null=True, help_text="Recomendaciones específicas de cuidado")
    tips = models.TextField(blank=True)
    curiosidades = models.TextField(blank=True, null=True, help_text="Datos interesantes o históricos")

    # Especificaciones botánicas
    altura_aproximada = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Altura promedio en cm")
    luz_recomendada = models.CharField(max_length=100, blank=True, null=True)
    riego = models.CharField(max_length=100, blank=True, null=True)
    temperatura_optima = models.CharField(max_length=50, blank=True, null=True)

    # Gestión
    sku = models.CharField(max_length=20, unique=True, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def get_tips_list(self):
        """Devuelve los tips como lista."""
        return [t.strip() for t in self.tips.splitlines() if t.strip()]

    def __str__(self):
        return self.nombre


    def get_tips_list(self):
        """Convierte el campo tips en lista separada por líneas."""
        return self.tips.splitlines()

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class ProductoEtiqueta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='etiquetas')
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'etiqueta')

    def __str__(self):
        return f"{self.producto.nombre} - {self.etiqueta.nombre}"




class Cliente(models.Model):
    """Perfil de cliente asociado a un usuario Django."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


# =========================
# PEDIDOS Y DETALLES
# =========================

class Pedido(models.Model):
    """Registro de pedidos realizados por clientes con soporte para Transbank, PayPal y otros."""

    # --------------------------
    # ESTADOS DEL PEDIDO
    # --------------------------
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('EP', 'Esperando Pago'),
        ('PA', 'Pagado'),
        ('R', 'Rechazado'),
        ('C', 'Cancelado'),
    ]

    TIPO_ENTREGA_CHOICES = [
        ('Despacho', 'Despacho a domicilio'),
        ('Retiro', 'Retiro en tienda'),
    ]

    # --------------------------
    # RELACIONES
    # --------------------------
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='pedidos'
    )
    productos = models.ManyToManyField(Producto, through='DetallePedido')

    # --------------------------
    # INFORMACIÓN GENERAL DEL PEDIDO
    # --------------------------
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='P')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --------------------------
    # ENTREGA
    # --------------------------
    tipo_entrega = models.CharField(
        max_length=20,
        choices=TIPO_ENTREGA_CHOICES,
        default='Despacho'
    )
    direccion_envio = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Dirección utilizada en este pedido."
    )

    # ================================
    # ⚡ CAMPOS PARA TRANSBANK
    # ================================
    transbank_token = models.CharField(max_length=100, blank=True, null=True)
    transbank_autorizacion = models.CharField(max_length=20, blank=True, null=True)
    transbank_tarjeta_tipo = models.CharField(max_length=5, blank=True, null=True)
    transbank_tarjeta_ultimos4 = models.CharField(max_length=4, blank=True, null=True)
    transbank_response = models.JSONField(blank=True, null=True)

    # ================================
    # 🌍 CAMPOS PARA PAYPAL
    # ================================
    paypal_order_id = models.CharField(max_length=200, blank=True, null=True)
    paypal_payer_id = models.CharField(max_length=200, blank=True, null=True)
    paypal_email = models.CharField(max_length=200, blank=True, null=True)
    paypal_status = models.CharField(max_length=100, blank=True, null=True)
    paypal_response = models.JSONField(blank=True, null=True)

    # ================================
    # METADATOS DE PAGO
    # ================================
    metodo_pago = models.CharField(max_length=50, default="Transbank")  # o "PayPal"

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.user.username}"



class DetallePedido(models.Model):
    """Detalle de productos asociados a un pedido."""
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='detalles'
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"


# =========================
# CARRITO DE COMPRAS
# =========================

class Carrito(models.Model):
    """Carrito de compras del cliente (1:1)."""
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.cliente.user.username}"


class ItemCarrito(models.Model):
    """Producto contenido dentro del carrito."""
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'producto')

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


# =========================
# SEÑALES
# =========================

