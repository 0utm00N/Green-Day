from core.models import Producto
from django.db import transaction

@transaction.atomic
def actualizar_datos_enriquecidos():

    data = {
    "Aloe Vera": {
        "categoria": "Suculenta",
        "descripcion_corta": "Planta medicinal y decorativa ideal para interiores luminosos.",
        "descripcion": "El Aloe Vera es una suculenta perenne muy valorada por sus propiedades curativas. "
                       "Tolera climas cálidos y secos, y sus hojas almacenan un gel con usos cosméticos y medicinales.",
        "tips": "Riega cada 2-3 semanas.\nEvita el exceso de agua.\nColoca en maceta con drenaje y sol directo.",
        "cuidados": "Prefiere suelos arenosos y luz intensa. Temperatura ideal entre 18°C y 25°C."
    },
    "Lavanda": {
        "categoria": "Aromática",
        "descripcion_corta": "Aromática resistente, ideal para jardines soleados.",
        "descripcion": "La Lavanda es una planta mediterránea muy apreciada por su fragancia y floración duradera. "
                       "Ideal para decorar exteriores, atraer abejas y perfumar el aire.",
        "tips": "Podar tras la floración.\nEvitar exceso de riego.\nColocar en zonas soleadas.",
        "cuidados": "Requiere pleno sol, suelo con buen drenaje y riego moderado."
    },
    "Menta": {
        "categoria": "Aromática",
        "descripcion_corta": "Hierba fresca ideal para infusiones, cócteles y cocina.",
        "descripcion": "La Menta es una planta vivaz y aromática de crecimiento rápido. "
                       "Requiere humedad constante y luz indirecta para mantener sus hojas tiernas y fragantes.",
        "tips": "Podar puntas regularmente.\nEvitar el sol directo fuerte.\nMantener humedad sin encharcar.",
        "cuidados": "Prefiere semisombra y riego frecuente. Ideal en macetas por su tendencia a expandirse."
    },
    "Romero": {
        "categoria": "Aromática",
        "descripcion_corta": "Planta mediterránea con aroma intenso y flores lilas.",
        "descripcion": "El Romero es una planta aromática muy resistente, símbolo de energía y memoria. "
                       "Ideal para climas secos y suelos bien drenados.",
        "tips": "Riego ligero.\nPodar al final del verano.\nExcelente como seto aromático.",
        "cuidados": "Prefiere sol directo, suelo seco y riego escaso."
    },
    "Cactus San Pedro": {
        "categoria": "Cactus",
        "descripcion_corta": "Cactus andino de rápido crecimiento y gran resistencia.",
        "descripcion": "Originario de los Andes, este cactus columnar puede alcanzar varios metros. "
                       "Muy resistente a la sequía y perfecto para exteriores soleados.",
        "tips": "Evitar riegos en invierno.\nUsar sustrato arenoso.\nProteger de heladas.",
        "cuidados": "Luz intensa y riego mensual. Temperaturas cálidas y baja humedad."
    },
    "Helecho Boston": {
        "categoria": "Interior",
        "descripcion_corta": "Planta frondosa ideal para interiores húmedos y sombreados.",
        "descripcion": "El Helecho Boston es una de las plantas más populares para interiores. "
                       "Purifica el aire y aporta un toque de frescura natural.",
        "tips": "Pulverizar agua sobre las hojas.\nEvitar sol directo.\nMantener humedad constante.",
        "cuidados": "Temperatura entre 18°C y 25°C. Luz difusa y riego frecuente."
    },
    "Suculenta Echeveria": {
        "categoria": "Suculenta",
        "descripcion_corta": "Planta ornamental de hojas simétricas y bajo mantenimiento.",
        "descripcion": "La Echeveria forma rosetas perfectas y es una de las suculentas más decorativas. "
                       "Ideal para interiores luminosos y jardines secos.",
        "tips": "Evitar exceso de agua.\nColocar en zona soleada.\nUsar sustrato con drenaje.",
        "cuidados": "Riego quincenal y exposición solar directa. Tolera sequía."
    },
    "Bonsái Ficus": {
        "categoria": "Bonsái",
        "descripcion_corta": "Mini árbol de interior símbolo de equilibrio y paciencia.",
        "descripcion": "El Bonsái Ficus es ideal para interiores. Representa armonía y perseverancia. "
                       "Sus raíces aéreas y hojas brillantes lo hacen muy apreciado.",
        "tips": "Poda ligera cada dos meses.\nRotar la maceta semanalmente.\nEvitar corrientes de aire.",
        "cuidados": "Luz indirecta, riego moderado y humedad constante."
    },
    "Geranio": {
        "categoria": "Flor",
        "descripcion_corta": "Flor colorida de exterior, resistente y de larga floración.",
        "descripcion": "El Geranio es una planta clásica de balcones y jardines. "
                       "Florece durante gran parte del año y soporta bien el sol directo.",
        "tips": "Eliminar flores secas.\nFertilizar cada 2 semanas.\nProteger del exceso de lluvia.",
        "cuidados": "Sol directo y riego moderado. Suelo bien drenado."
    },
    "Orquídea Phalaenopsis": {
        "categoria": "Flor",
        "descripcion_corta": "Orquídea elegante y de cuidados simples.",
        "descripcion": "Conocida como la ‘orquídea mariposa’, es ideal para interiores luminosos. "
                       "Su floración puede durar varios meses.",
        "tips": "Usar agua sin cal.\nEvitar sol directo.\nPodar tallos tras la floración.",
        "cuidados": "Temperatura entre 18°C y 26°C, humedad alta y sustrato de corteza."
    },
    "Potus": {
        "categoria": "Interior",
        "descripcion_corta": "Planta trepadora resistente y purificadora de aire.",
        "descripcion": "El Potus es una planta de interior de fácil cuidado. "
                       "Crece rápidamente y se adapta a distintas condiciones lumínicas.",
        "tips": "Riego semanal.\nEvitar exceso de agua.\nIdeal para colgar o guiar.",
        "cuidados": "Luz media e indirecta, riego moderado. Muy tolerante al descuido."
    },
    "Peperomia": {
        "categoria": "Interior",
        "descripcion_corta": "Planta compacta de hojas carnosas y aspecto brillante.",
        "descripcion": "La Peperomia es ideal para espacios pequeños. "
                       "Sus hojas almacenan agua, lo que la hace fácil de mantener.",
        "tips": "Evitar sol directo.\nRiego moderado.\nNo pulverizar sus hojas.",
        "cuidados": "Temperatura templada y suelo con drenaje. Riego cada 10 días."
    },
    "Cinta (Malamadre)": {
        "categoria": "Interior",
        "descripcion_corta": "Colgante resistente que purifica el aire y tolera poca luz.",
        "descripcion": "La Cinta es una planta resistente, ideal para principiantes. "
                       "Purifica el aire y crece en casi cualquier ambiente.",
        "tips": "Riego moderado.\nPodar hojas secas.\nResiste poca luz.",
        "cuidados": "Luz indirecta, riego semanal y buena ventilación."
    },
    "Ficus Lyrata": {
        "categoria": "Tropical",
        "descripcion_corta": "Planta grande con hojas tipo violín, muy decorativa.",
        "descripcion": "El Ficus Lyrata es una planta tropical de gran porte, ideal para interiores amplios y luminosos.",
        "tips": "Limpiar hojas con paño húmedo.\nEvitar corrientes de aire.\nNo moverla con frecuencia.",
        "cuidados": "Temperaturas entre 20°C y 27°C. Luz brillante indirecta y riego cada 10 días."
    },
    "Monstera Deliciosa": {
        "categoria": "Tropical",
        "descripcion_corta": "Planta tropical icónica con hojas perforadas.",
        "descripcion": "La Monstera, también conocida como Costilla de Adán, es símbolo de elegancia natural. "
                       "Sus hojas grandes aportan un toque exótico a cualquier ambiente.",
        "tips": "Evitar sol directo.\nUsar tutor para sostener el tallo.\nPulverizar agua sobre hojas.",
        "cuidados": "Luz filtrada, riego semanal y humedad ambiental constante."
    },
    "Calathea": {
        "categoria": "Interior",
        "descripcion_corta": "Planta de hojas decorativas con patrones únicos.",
        "descripcion": "La Calathea destaca por sus hojas coloridas y su capacidad de moverse según la luz del día.",
        "tips": "Evitar sol directo.\nPulverizar con agua.\nNo usar agua calcárea.",
        "cuidados": "Alta humedad, riego frecuente y luz difusa."
    },
    "Drácena Marginata": {
        "categoria": "Tropical",
        "descripcion_corta": "Planta esbelta de hojas finas, perfecta para oficinas.",
        "descripcion": "La Drácena Marginata es muy valorada por su elegancia y resistencia. "
                       "Ayuda a purificar el aire y soporta entornos de baja luz.",
        "tips": "No regar en exceso.\nEvitar corrientes de aire.\nGirar cada semana.",
        "cuidados": "Luz media, riego cada 10-12 días. Temperatura 18–26°C."
    },
    "Sansevieria (Lengua de Suegra)": {
        "categoria": "Suculenta",
        "descripcion_corta": "Planta extremadamente resistente, ideal para principiantes.",
        "descripcion": "La Sansevieria es una planta de interior que tolera casi cualquier condición. "
                       "Purifica el aire y apenas requiere mantenimiento.",
        "tips": "Riego mensual.\nTolera poca luz.\nEvitar exceso de agua.",
        "cuidados": "Luz indirecta y suelo seco. Muy resistente al abandono."
    },
    "Suculenta Haworthia": {
        "categoria": "Suculenta",
        "descripcion_corta": "Mini suculenta compacta y resistente, ideal para interiores.",
        "descripcion": "La Haworthia es una pequeña suculenta sudafricana de hojas carnosas y translúcidas.",
        "tips": "Regar cada 2 semanas.\nUsar sustrato arenoso.\nEvitar sol directo fuerte.",
        "cuidados": "Luz brillante indirecta, riego escaso y suelo bien drenado."
    },
    "Fresia": {
        "categoria": "Flor",
        "descripcion_corta": "Flor aromática y colorida ideal para jardines primaverales.",
        "descripcion": "La Fresia ofrece flores fragantes en tonos vivos, muy usadas en arreglos florales.",
        "tips": "Riego moderado.\nProteger de heladas.\nPlantar en suelos drenados.",
        "cuidados": "Prefiere sol pleno y suelos fértiles. Riego regular durante la floración."
    },
    "Hiedra": {
        "categoria": "Trepadora",
        "descripcion_corta": "Planta trepadora versátil para interiores o exteriores.",
        "descripcion": "La Hiedra es una planta de rápido crecimiento que se adapta a distintas condiciones.",
        "tips": "Poda frecuente.\nEvitar exceso de riego.\nIdeal para colgar o guiar.",
        "cuidados": "Semisombra y riego moderado. Tolera bajas temperaturas."
    },
    "Crisantemo": {
        "categoria": "Flor",
        "descripcion_corta": "Flor otoñal de colores intensos y fácil cultivo.",
        "descripcion": "El Crisantemo florece en otoño y simboliza alegría y vitalidad. "
                       "Se adapta bien a climas templados.",
        "tips": "Eliminar flores marchitas.\nFertilizar en floración.\nEvitar heladas.",
        "cuidados": "Sol directo y riego frecuente sin encharcar."
    },
    "Tulipán": {
        "categoria": "Flor",
        "descripcion_corta": "Flor de primavera elegante y simbólica.",
        "descripcion": "El Tulipán es una planta bulbosa que florece en primavera. "
                       "Su forma y color la hacen símbolo de amor y esperanza.",
        "tips": "Plantar en invierno.\nProteger del exceso de humedad.\nCortar flores marchitas.",
        "cuidados": "Climas fríos y suelos fértiles. Riego moderado."
    },
    "Rosa Miniatura": {
        "categoria": "Flor",
        "descripcion_corta": "Versión compacta de la rosa tradicional, ideal para interiores.",
        "descripcion": "Las Rosas Miniatura ofrecen flores pequeñas y coloridas durante casi todo el año.",
        "tips": "Riego constante sin encharcar.\nPodar ramas secas.\nExposición al sol directo.",
        "cuidados": "Suelos fértiles, sol pleno y riego frecuente en verano."
    },
    "Bromelia": {
        "categoria": "Tropical",
        "descripcion_corta": "Planta tropical colorida de alta humedad.",
        "descripcion": "La Bromelia es una planta exótica que destaca por su flor central y hojas rosetadas.",
        "tips": "Mantener agua en el centro de la roseta.\nEvitar sol directo.\nAlta humedad.",
        "cuidados": "Luz difusa, riego interno en la copa y temperatura templada."
    },
    "Palmera Areca": {
        "categoria": "Tropical",
        "descripcion_corta": "Palmera elegante y purificadora, ideal para interiores amplios.",
        "descripcion": "La Areca es una planta tropical muy valorada por su elegancia y capacidad para purificar el aire.",
        "tips": "Pulverizar hojas.\nEvitar luz directa intensa.\nMantener suelo húmedo.",
        "cuidados": "Luz brillante, riego constante y alta humedad ambiental."
    },
    "Begonia Rex": {
        "categoria": "Interior",
        "descripcion_corta": "Planta de hojas coloridas, ideal para decorar interiores.",
        "descripcion": "La Begonia Rex destaca por su follaje vibrante. No requiere luz intensa, pero sí humedad estable.",
        "tips": "No mojar hojas.\nEvitar corrientes de aire.\nMantener temperatura constante.",
        "cuidados": "Semisombra, riego regular y alta humedad ambiental."
    },
    "Anturio": {
        "categoria": "Flor",
        "descripcion_corta": "Flor tropical brillante, símbolo de elegancia.",
        "descripcion": "El Anturio se distingue por su flor roja brillante y su longevidad. "
                       "Ideal para interiores luminosos y húmedos.",
        "tips": "Pulverizar hojas.\nEvitar sol directo.\nRiego frecuente en verano.",
        "cuidados": "Luz indirecta intensa, humedad alta y sustrato ligero."
    },
    "Cactus Bola de Oro": {
        "categoria": "Cactus",
        "descripcion_corta": "Cactus redondo y espinoso, de gran resistencia.",
        "descripcion": "El Cactus Bola de Oro es ideal para exteriores soleados. "
                       "Su forma esférica y color dorado lo hacen muy decorativo.",
        "tips": "No regar en invierno.\nExposición solar plena.\nSustrato arenoso.",
        "cuidados": "Riego mensual y sol directo. Tolera altas temperaturas."
    },
    "Jazmín": {
        "categoria": "Trepadora",
        "descripcion_corta": "Planta trepadora de flores blancas y aroma intenso.",
        "descripcion": "El Jazmín es una planta ornamental clásica, símbolo de pureza y amor. "
                       "Sus flores perfuman el ambiente durante la primavera y verano.",
        "tips": "Riego frecuente.\nExposición al sol.\nPodar tras la floración.",
        "cuidados": "Pleno sol, riego constante y suelo fértil con buen drenaje."
    }
}


    total = 0
    no_encontrados = []
    for nombre, datos in data.items():
        try:
            producto = Producto.objects.get(nombre=nombre)
            producto.descripcion_corta = datos["descripcion_corta"]
            producto.descripcion = datos["descripcion"]
            producto.categoria = datos["categoria"]
            producto.cuidados = datos["cuidados"]
            producto.tips = datos["tips"]

            producto.save()
            print(f"✅ {nombre} actualizado.")
            total += 1
        except Producto.DoesNotExist:
            print(f"⚠️ No se encontró: {nombre}")

    print(f"\n🌱 Total de productos enriquecidos: {total}")
    if no_encontrados:
        print(f"⚠️ Productos no encontrados: {', '.join(no_encontrados)}")
    else:
        print("✅ Todos los productos fueron encontrados y actualizados correctamente.")

    return total


if __name__ == "__main__":
    actualizar_datos_enriquecidos()


