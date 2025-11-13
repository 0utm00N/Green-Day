console.log("✅ catalogo.js cargado correctamente");

document.addEventListener("DOMContentLoaded", () => {
    inicializarControlesCantidad();
    inicializarBotonesAgregar();
});

// ============================
// CONTROL DE CANTIDAD
// ============================
function inicializarControlesCantidad() {
    document.querySelectorAll(".quantity-selector").forEach(selector => {
        const stock = parseInt(selector.dataset.stock) || 99;
        const spanCantidad = selector.querySelector(".quantity");
        const botones = selector.querySelectorAll(".btn-quantity");
        const btnMenos = botones[0];
        const btnMas = botones[1];

        btnMenos.addEventListener("click", () => {
            let valor = parseInt(spanCantidad.textContent);
            if (valor > 1) {
                spanCantidad.textContent = valor - 1;
            }
        });

        btnMas.addEventListener("click", () => {
            let valor = parseInt(spanCantidad.textContent);
            if (valor < stock) {
                spanCantidad.textContent = valor + 1;
            }
        });
    });
}

// ============================
// BOTÓN "AGREGAR AL CARRITO"
// ============================
function inicializarBotonesAgregar() {
    document.querySelectorAll(".btn-agregar").forEach(boton => {
        boton.addEventListener("click", async () => {
            const productoId = boton.dataset.id;
            const acciones = boton.closest(".acciones");
            const cantidadSpan = acciones.querySelector(".quantity");
            const cantidad = parseInt(cantidadSpan.textContent);

            // Mostrar en consola lo que se va a enviar
            console.log(`🛒 Enviando producto ${productoId} con cantidad ${cantidad}`);

            try {
                const response = await fetch(`/agregar/${productoId}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": getCookie("csrftoken"),
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    body: `cantidad=${cantidad}`
                });

                const data = await response.json();
                console.log("📦 Respuesta del servidor:", data);

                if (data.success) {
                    actualizarContadorCarrito(data.count);
                    mostrarToast(`✅ Se agregaron ${cantidad} unidad(es) de ${data.producto} al carrito.`);
                } else {
                    mostrarToast(`⚠️ ${data.error || "Ocurrió un error al agregar al carrito."}`);
                }
            } catch (error) {
                console.error("❌ Error en fetch:", error);
                mostrarToast("⚠️ Error de red al agregar al carrito.");
            }
        });
    });
}

// ============================
// ACTUALIZAR CONTADOR
// ============================
function actualizarContadorCarrito(total) {
    const contador = document.getElementById("contador-carrito");
    if (contador) contador.textContent = total;
}

// ============================
// TOAST / MENSAJE VISUAL
// ============================
function mostrarToast(mensaje) {
    const toast = document.createElement("div");
    toast.textContent = mensaje;
    Object.assign(toast.style, {
        position: "fixed",
        bottom: "20px",
        right: "20px",
        backgroundColor: "#00c896",
        color: "#121212",
        padding: "12px 18px",
        borderRadius: "10px",
        fontWeight: "bold",
        zIndex: "9999",
        boxShadow: "0 3px 10px rgba(0,0,0,0.4)",
        opacity: "1",
        transition: "opacity 0.3s ease",
    });
    document.body.appendChild(toast);

    // Desaparece en 2 segundos
    setTimeout(() => { toast.style.opacity = "0"; }, 1800);
    setTimeout(() => { toast.remove(); }, 2100);
}

// ============================
// OBTENER TOKEN CSRF
// ============================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
