# -*- coding: utf-8 -*-
"""
Inyecta datos enriquecidos (nombre_cientifico, curiosidades, altura_aproximada,
luz_recomendada, riego, temperatura_optima, sku) para 30 plantas.
Si OVERWRITE=False solo completa campos vacíos; si True, sobrescribe.
"""

from django.db import transaction
from django.utils.text import slugify

from core.models import Producto

# Cambia a True si quieres sobrescribir lo ya existente
OVERWRITE = False

DATA = {
    "Aloe Vera": {
        "nombre_cientifico": "Aloe vera",
        "curiosidades": "Su gel se usa desde el Antiguo Egipto con fines cosméticos y calmantes.",
        "altura_aproximada": 40,
        "luz_recomendada": "Pleno sol / Luz brillante",
        "riego": "Escaso",
        "temperatura_optima": "18°C – 25°C",
    },
    "Lavanda": {
        "nombre_cientifico": "Lavandula angustifolia",
        "curiosidades": "Los romanos perfumaban baños con lavanda; atrae polinizadores.",
        "altura_aproximada": 60,
        "luz_recomendada": "Pleno sol",
        "riego": "Escaso a moderado",
        "temperatura_optima": "15°C – 28°C",
    },
    "Menta": {
        "nombre_cientifico": "Mentha spicata",
        "curiosidades": "Crece vigorosa y puede volverse invasiva; ideal en maceta.",
        "altura_aproximada": 35,
        "luz_recomendada": "Semisombra / Luz indirecta",
        "riego": "Frecuente",
        "temperatura_optima": "15°C – 25°C",
    },
    "Romero": {
        "nombre_cientifico": "Salvia rosmarinus",
        "curiosidades": "Símbolo de memoria en la tradición europea; muy melífera.",
        "altura_aproximada": 80,
        "luz_recomendada": "Pleno sol",
        "riego": "Escaso",
        "temperatura_optima": "12°C – 28°C",
    },
    "Cactus San Pedro": {
        "nombre_cientifico": "Echinopsis pachanoi",
        "curiosidades": "Cactus andino de rápido crecimiento; muy usado como patrón ornamental.",
        "altura_aproximada": 150,
        "luz_recomendada": "Pleno sol",
        "riego": "Muy escaso",
        "temperatura_optima": "18°C – 30°C",
    },
    "Helecho Boston": {
        "nombre_cientifico": "Nephrolepis exaltata ‘Bostoniensis’",
        "curiosidades": "Clásico de interiores por su follaje colgante y capacidad de purificar aire.",
        "altura_aproximada": 60,
        "luz_recomendada": "Luz indirecta",
        "riego": "Frecuente (humedad alta)",
        "temperatura_optima": "18°C – 25°C",
    },
    "Suculenta Echeveria": {
        "nombre_cientifico": "Echeveria elegans",
        "curiosidades": "Forma rosetas perfectas; muy usada en xerojardinería.",
        "altura_aproximada": 15,
        "luz_recomendada": "Luz brillante / Pleno sol suave",
        "riego": "Escaso",
        "temperatura_optima": "18°C – 26°C",
    },
    "Bonsái Ficus": {
        "nombre_cientifico": "Ficus microcarpa",
        "curiosidades": "Popular como bonsái por su tolerancia y raíces aéreas.",
        "altura_aproximada": 35,
        "luz_recomendada": "Luz brillante indirecta",
        "riego": "Moderado",
        "temperatura_optima": "18°C – 28°C",
    },
    "Geranio": {
        "nombre_cientifico": "Pelargonium × hortorum",
        "curiosidades": "Emblema de balcones mediterráneos; floración casi todo el año.",
        "altura_aproximada": 45,
        "luz_recomendada": "Pleno sol",
        "riego": "Moderado",
        "temperatura_optima": "15°C – 28°C",
    },
    "Orquídea Phalaenopsis": {
        "nombre_cientifico": "Phalaenopsis (híbridos)",
        "curiosidades": "‘Orquídea mariposa’; su floración puede durar meses.",
        "altura_aproximada": 45,
        "luz_recomendada": "Luz brillante filtrada",
        "riego": "Moderado (sustrato de corteza)",
        "temperatura_optima": "18°C – 26°C",
    },
    "Potus": {
        "nombre_cientifico": "Epipremnum aureum",
        "curiosidades": "Muy tolerante; ideal para principiantes y espacios colgantes.",
        "altura_aproximada": 200,  # longitud de bejucos
        "luz_recomendada": "Luz media/indirecta",
        "riego": "Moderado",
        "temperatura_optima": "18°C – 28°C",
    },
    "Peperomia": {
        "nombre_cientifico": "Peperomia obtusifolia",
        "curiosidades": "Hojas carnosas que almacenan agua; gran variedad de cultivares.",
        "altura_aproximada": 25,
        "luz_recomendada": "Luz indirecta",
        "riego": "Moderado (dejar secar ligeramente)",
        "temperatura_optima": "18°C – 26°C",
    },
    "Cinta (Malamadre)": {
        "nombre_cientifico": "Chlorophytum comosum",
        "curiosidades": "Purificadora de aire; produce ‘hijitos’ fácilmente.",
        "altura_aproximada": 30,
        "luz_recomendada": "Luz indirecta / Semisombra",
        "riego": "Moderado",
        "temperatura_optima": "16°C – 26°C",
    },
    "Ficus Lyrata": {
        "nombre_cientifico": "Ficus lyrata",
        "curiosidades": "Hojas en forma de violín; ícono del diseño de interiores.",
        "altura_aproximada": 180,
        "luz_recomendada": "Luz brillante indirecta",
        "riego": "Moderado (sin encharcar)",
        "temperatura_optima": "20°C – 27°C",
    },
    "Monstera Deliciosa": {
        "nombre_cientifico": "Monstera deliciosa",
        "curiosidades": "‘Costilla de Adán’; sus perforaciones aumentan con la edad.",
        "altura_aproximada": 200,
        "luz_recomendada": "Luz brillante filtrada",
        "riego": "Moderado",
        "temperatura_optima": "20°C – 28°C",
    },
    "Calathea": {
        "nombre_cientifico": "Calathea spp.",
        "curiosidades": "‘Plantas que oran’: mueven hojas según la luz.",
        "altura_aproximada": 60,
        "luz_recomendada": "Luz difusa (sin sol directo)",
        "riego": "Frecuente (humedad alta)",
        "temperatura_optima": "18°C – 26°C",
    },
    "Drácena Marginata": {
        "nombre_cientifico": "Dracaena marginata",
        "curiosidades": "Gran purificadora; muy usada en oficinas por su resistencia.",
        "altura_aproximada": 150,
        "luz_recomendada": "Luz media",
        "riego": "Moderado-escaso",
        "temperatura_optima": "18°C – 26°C",
    },
    "Sansevieria (Lengua de Suegra)": {
        "nombre_cientifico": "Dracaena trifasciata (Sansevieria)",
        "curiosidades": "Tolera olvidos prolongados; ideal para principiantes.",
        "altura_aproximada": 70,
        "luz_recomendada": "Luz indirecta / Poca luz",
        "riego": "Muy escaso",
        "temperatura_optima": "15°C – 30°C",
    },
    "Suculenta Haworthia": {
        "nombre_cientifico": "Haworthiopsis attenuata",
        "curiosidades": "Sus bandas blancas la hacen muy ornamental en mini jardines.",
        "altura_aproximada": 12,
        "luz_recomendada": "Luz brillante indirecta",
        "riego": "Escaso",
        "temperatura_optima": "18°C – 26°C",
    },
    "Fresia": {
        "nombre_cientifico": "Freesia refracta",
        "curiosidades": "Muy valorada en perfumería por su fragancia dulce.",
        "altura_aproximada": 35,
        "luz_recomendada": "Pleno sol / Luz brillante",
        "riego": "Moderado",
        "temperatura_optima": "12°C – 22°C",
    },
    "Hiedra": {
        "nombre_cientifico": "Hedera helix",
        "curiosidades": "Trepadora clásica; excelente colgante en interior.",
        "altura_aproximada": 300,  # longitud de guías
        "luz_recomendada": "Semisombra / Luz media",
        "riego": "Moderado",
        "temperatura_optima": "10°C – 24°C",
    },
    "Crisantemo": {
        "nombre_cientifico": "Chrysanthemum morifolium",
        "curiosidades": "Flor emblemática del otoño; símbolo de longevidad en Asia.",
        "altura_aproximada": 50,
        "luz_recomendada": "Pleno sol",
        "riego": "Frecuente en floración",
        "temperatura_optima": "12°C – 20°C",
    },
    "Tulipán": {
        "nombre_cientifico": "Tulipa gesneriana",
        "curiosidades": "Protagonista de la ‘tulipomanía’ neerlandesa del s. XVII.",
        "altura_aproximada": 40,
        "luz_recomendada": "Pleno sol",
        "riego": "Moderado (bulbo en reposo seco)",
        "temperatura_optima": "5°C – 18°C (requiere frío invernal)",
    },
    "Rosa Miniatura": {
        "nombre_cientifico": "Rosa chinensis (mini)",
        "curiosidades": "Selecciones compactas que florecen en ciclos muy seguidos.",
        "altura_aproximada": 35,
        "luz_recomendada": "Pleno sol",
        "riego": "Frecuente sin encharcar",
        "temperatura_optima": "15°C – 26°C",
    },
    "Bromelia": {
        "nombre_cientifico": "Guzmania lingulata",
        "curiosidades": "Acumula agua en su ‘copa’; inflorescencia muy duradera.",
        "altura_aproximada": 45,
        "luz_recomendada": "Luz brillante indirecta",
        "riego": "Moderado (agua en la roseta)",
        "temperatura_optima": "18°C – 28°C",
    },
    "Palmera Areca": {
        "nombre_cientifico": "Dypsis lutescens",
        "curiosidades": "Conocida como ‘palmera bambú’; excelente purificadora.",
        "altura_aproximada": 200,
        "luz_recomendada": "Luz brillante indirecta",
        "riego": "Moderado-frecuente",
        "temperatura_optima": "18°C – 28°C",
    },
    "Begonia Rex": {
        "nombre_cientifico": "Begonia rex-cultorum",
        "curiosidades": "Famosa por su follaje iridiscente y patrones únicos.",
        "altura_aproximada": 30,
        "luz_recomendada": "Luz difusa",
        "riego": "Moderado (no mojar hojas)",
        "temperatura_optima": "18°C – 24°C",
    },
    "Anturio": {
        "nombre_cientifico": "Anthurium andraeanum",
        "curiosidades": "La ‘flor’ roja es en realidad una espata; muy longevo en florero.",
        "altura_aproximada": 60,
        "luz_recomendada": "Luz brillante indirecta",
        "riego": "Frecuente (alta humedad)",
        "temperatura_optima": "18°C – 28°C",
    },
    "Cactus Bola de Oro": {
        "nombre_cientifico": "Echinocactus grusonii",
        "curiosidades": "También llamado ‘asiento de suegra’; muy longevo.",
        "altura_aproximada": 40,
        "luz_recomendada": "Pleno sol",
        "riego": "Muy escaso",
        "temperatura_optima": "20°C – 35°C (seco)",
    },
    "Jazmín": {
        "nombre_cientifico": "Jasminum officinale",
        "curiosidades": "Aroma icónico en perfumería; trepadora de rápido crecimiento.",
        "altura_aproximada": 300,
        "luz_recomendada": "Pleno sol",
        "riego": "Frecuente en temporada cálida",
        "temperatura_optima": "15°C – 28°C",
    },
}


def _maybe_set(obj, field, value):
    """Setea si OVERWRITE=True o si el campo está vacío/None."""
    current = getattr(obj, field, None)
    if OVERWRITE or current in (None, "", 0):
        setattr(obj, field, value)


@transaction.atomic
def run():
    total_ok = 0
    missing = []

    for nombre, datos in DATA.items():
        try:
            p = Producto.objects.get(nombre=nombre)

            _maybe_set(p, "nombre_cientifico", datos["nombre_cientifico"])
            _maybe_set(p, "curiosidades", datos["curiosidades"])
            _maybe_set(p, "altura_aproximada", datos["altura_aproximada"])
            _maybe_set(p, "luz_recomendada", datos["luz_recomendada"])
            _maybe_set(p, "riego", datos["riego"])
            _maybe_set(p, "temperatura_optima", datos["temperatura_optima"])

            # SKU estable: si no existe o si OVERWRITE, genera GD-<slug>-<id4>
            if OVERWRITE or not p.sku:
                base = slugify(p.nombre)[:12]  # más corto/limpio
                p.sku = f"GD-{base}-{p.id:04d}"

            p.save()
            print(f"✅ {p.nombre} actualizado.")
            total_ok += 1

        except Producto.DoesNotExist:
            missing.append(nombre)

    print(f"\n🌿 Total de productos enriquecidos: {total_ok}")
    if missing:
        print(f"⚠️ No encontrados ({len(missing)}): {', '.join(missing)}")
    else:
        print("✨ Todos los productos del catálogo fueron actualizados.")


if __name__ == "__main__":
    run()
