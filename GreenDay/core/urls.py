from django.urls import path
from . import views

urlpatterns = [
    # -----------------------------
    # Home
    # -----------------------------
    path('', views.home, name='home'),

    # -----------------------------
    # Catálogo
    # -----------------------------
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),

    # -----------------------------
    # Carrito
    # -----------------------------
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/', views.eliminar_del_carrito, name='eliminar_item_carrito'),
    path('api/carrito/contador/', views.contador_carrito, name='contador_carrito'),
    path('carrito/despacho/', views.opcion_despacho, name='opcion_despacho'),
    path('carrito/retiro/', views.opcion_retiro, name='opcion_retiro'),

    # -----------------------------
    # Pedidos
    # -----------------------------
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedidos/', views.historial_pedidos, name='historial_pedidos'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedido-exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),

    # -----------------------------
    # Perfil
    # -----------------------------
    path('perfil/', views.ver_perfil, name='ver_perfil'),

    # -----------------------------
    # Login / Logout
    # -----------------------------
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # -----------------------------
    # Pagos simulados
    # -----------------------------
    path("transbank/confirmar/", views.confirmar_transbank, name="confirmar_transbank"),
    path("paypal/confirmar/", views.confirmar_paypal, name="confirmar_paypal"),
    path("paypal/cancelado/", views.paypal_cancelado, name="paypal_cancelado"),
]
