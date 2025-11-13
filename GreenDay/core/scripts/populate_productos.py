# core/populate_productos.py

from core.models import Producto, Invernadero

def poblar_productos():
    # ⚠️ Asegúrate de tener un invernadero ya creado
    invernadero = Invernadero.objects.first()
    if not invernadero:
        print("❌ No hay ningún invernadero. Crea uno primero desde el admin.")
        return

    productos = [
        {"nombre": "Aloe Vera", "descripcion": "Planta suculenta medicinal. Requiere sol directo y poco riego.", "precio": 3500, "stock": 10},
        {"nombre": "Lavanda", "descripcion": "Aromática ideal para relajar. Requiere sol pleno y suelo seco.", "precio": 2800, "stock": 15},
        {"nombre": "Menta", "descripcion": "Planta aromática para infusiones. Mantener húmeda y en semisombra.", "precio": 2500, "stock": 20},
        {"nombre": "Romero", "descripcion": "Hierba aromática resistente a la sequía. Pleno sol.", "precio": 2600, "stock": 12},
        {"nombre": "Cactus San Pedro", "descripcion": "Cactus de rápido crecimiento. Riego muy escaso.", "precio": 4000, "stock": 8},
        {"nombre": "Helecho Boston", "descripcion": "Ideal para interiores húmedos. Luz indirecta.", "precio": 3300, "stock": 14},
        {"nombre": "Suculenta Echeveria", "descripcion": "Decorativa y de bajo mantenimiento. Mucha luz y poco agua.", "precio": 2900, "stock": 16},
        {"nombre": "Bonsái Ficus", "descripcion": "Mini árbol de interior. Mantener suelo húmedo y luz filtrada.", "precio": 8500, "stock": 5},
        {"nombre": "Geranio", "descripcion": "Flor colorida de exterior. Riego moderado y pleno sol.", "precio": 3100, "stock": 18},
        {"nombre": "Orquídea Phalaenopsis", "descripcion": "Flor elegante de interior. Evitar sol directo.", "precio": 9700, "stock": 7},
        {"nombre": "Potus", "descripcion": "Treparora interior. Luz media y riego semanal.", "precio": 2700, "stock": 20},
        {"nombre": "Peperomia", "descripcion": "Compacta y fácil de cuidar. Luz indirecta.", "precio": 2900, "stock": 15},
        {"nombre": "Cinta (Malamadre)", "descripcion": "Purifica el aire. Ideal para colgar.", "precio": 2600, "stock": 20},
        {"nombre": "Ficus Lyrata", "descripcion": "Planta grande de interior. Mucha luz sin sol directo.", "precio": 7800, "stock": 6},
        {"nombre": "Monstera Deliciosa", "descripcion": "De hojas grandes y tropicales. Luz brillante filtrada.", "precio": 7200, "stock": 9},
        {"nombre": "Calathea", "descripcion": "De hojas ornamentales. Evitar sol directo, mantener humedad.", "precio": 6900, "stock": 10},
        {"nombre": "Drácena Marginata", "descripcion": "Tropical resistente. Poca agua y luz media.", "precio": 6200, "stock": 11},
        {"nombre": "Sansevieria (Lengua de Suegra)", "descripcion": "Muy resistente. Ideal para principiantes.", "precio": 3000, "stock": 22},
        {"nombre": "Suculenta Haworthia", "descripcion": "Perfecta para interiores. Riego cada 2 semanas.", "precio": 2500, "stock": 19},
        {"nombre": "Fresia", "descripcion": "Flor aromática. Prefiere sol y riego moderado.", "precio": 2800, "stock": 15},
        {"nombre": "Hiedra", "descripcion": "Trepa fácilmente. Evitar sol fuerte.", "precio": 2700, "stock": 16},
        {"nombre": "Crisantemo", "descripcion": "Flor otoñal. Mucha luz y riego frecuente.", "precio": 3200, "stock": 10},
        {"nombre": "Tulipán", "descripcion": "Flor de primavera. Requiere frío invernal.", "precio": 4800, "stock": 8},
        {"nombre": "Rosa Miniatura", "descripcion": "Flores pequeñas. Sol directo y buen drenaje.", "precio": 5600, "stock": 9},
        {"nombre": "Bromelia", "descripcion": "Colorida y tropical. Requiere humedad.", "precio": 7100, "stock": 7},
        {"nombre": "Palmera Areca", "descripcion": "Ideal para interiores amplios. Luz brillante.", "precio": 8200, "stock": 5},
        {"nombre": "Begonia Rex", "descripcion": "De hojas coloridas. No tolera sol directo.", "precio": 6600, "stock": 12},
        {"nombre": "Anturio", "descripcion": "De flor roja brillante. Luz indirecta y alta humedad.", "precio": 8500, "stock": 6},
        {"nombre": "Cactus Bola de Oro", "descripcion": "Cactus redondo y espinoso. Muy resistente.", "precio": 3700, "stock": 10},
        {"nombre": "Jazmín", "descripcion": "Flor fragante. Necesita sol directo y riego regular.", "precio": 4900, "stock": 8},
    ]

    for p in productos:
        Producto.objects.create(
            nombre=p["nombre"],
            descripcion=p["descripcion"],
            precio=p["precio"],
            stock=p["stock"],
            invernadero=invernadero
        )

    print("✅ Se han insertado los 30 productos correctamente.")

