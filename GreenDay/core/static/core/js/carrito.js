console.log("✅ carrito.js cargado correctamente");

// --------------------------
// Actualizar contador del carrito
// --------------------------
function actualizarContadorCarrito() {
    fetch(contadorUrl)
        .then(response => response.json())
        .then(data => {
            const contador = document.getElementById("contador-carrito");
            if (contador) contador.textContent = data.count;
        })
        .catch(err => console.error("Error al actualizar contador:", err));
}

// --------------------------
// CSRF Helper
// --------------------------
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

// --------------------------
// Agregar productos al carrito
// --------------------------
document.addEventListener("DOMContentLoaded", () => {
    const botones = document.querySelectorAll(".btn-agregar");
    const csrftoken = getCookie("csrftoken");

    if (botones.length === 0) {
        console.log("ℹ️ No hay botones de agregar al carrito en esta página.");
    } else {
        botones.forEach(boton => {
            boton.addEventListener("click", () => {
                const productoId = boton.dataset.id;
                console.log(`🛒 Agregando producto ID ${productoId}`);

                fetch(`/agregar/${productoId}/`, {
                    method: "POST",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrftoken,
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log(`✅ Producto agregado: ${data.producto}`);
                        actualizarContadorCarrito();
                    } else {
                        console.error("❌ Error al agregar:", data.error);
                    }
                })
                .catch(error => console.error("Error en fetch:", error));
            });
        });
    }
});

// --------------------------
// Eliminar productos del carrito
// --------------------------
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".btn-eliminar").forEach(btn => {
        btn.addEventListener("click", function () {
            const productoId = this.dataset.id;

            fetch("/carrito/eliminar/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "producto_id=" + productoId
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const itemElement = document.getElementById("item-" + productoId);
                    if (itemElement) {
                        itemElement.style.opacity = "0";
                        setTimeout(() => itemElement.remove(), 300);
                    }
                    actualizarContadorCarrito();
                } else {
                    console.error("Error al eliminar:", data.error);
                }
            })
            .catch(err => console.error("Error en fetch eliminar:", err));
        });
    });
});

// --------------------------
// Validación de pago, entrega y dirección
// --------------------------
document.addEventListener("DOMContentLoaded", () => {

    console.log("🟢 Validación completa activada");

    const btnFinalizar = document.getElementById("btn-finalizar");

    // Inputs principales
    const inputPagos = document.querySelectorAll(".input-pago");
    const inputEntregas = document.querySelectorAll(".input-entrega");

    // Sección dirección
    const direccionBlock = document.getElementById("bloque-direccion");
    const direccionOptions = document.querySelectorAll(".input-direccion");
    const nuevaDireccionCampo = document.getElementById("campo-nueva-direccion");
    const inputNuevaDireccion = document.getElementById("direccion_nueva");

    // Campos ocultos para el servidor
    const hiddenPago = document.getElementById("metodo_pago_final");
    const hiddenEntrega = document.getElementById("metodo_entrega_final");
    const hiddenDireccion = document.getElementById("direccion_final");

    function validarTodo() {
        const pagoSeleccionado = document.querySelector(".input-pago:checked");
        const entregaSeleccionada = document.querySelector(".input-entrega:checked");

        let direccionValida = false;

        // Si eligió retiro → dirección no es necesaria
        if (entregaSeleccionada && entregaSeleccionada.value === "retiro") {
            direccionValida = true;
            hiddenDireccion.value = "retiro";
        }

        // Si eligió despacho → revisar opciones de dirección
        if (entregaSeleccionada && entregaSeleccionada.value === "despacho") {
            const direccionSel = document.querySelector(".input-direccion:checked");

            if (direccionSel) {
                if (direccionSel.value === "guardada") {
                    direccionValida = true;
                    hiddenDireccion.value = "guardada";
                }

                if (direccionSel.value === "nueva") {
                    if (inputNuevaDireccion.value.trim().length > 5) {
                        direccionValida = true;
                        hiddenDireccion.value = inputNuevaDireccion.value.trim();
                    } else {
                        direccionValida = false;
                    }
                }
            }
        }

        // Guardar valores finales
        if (pagoSeleccionado) hiddenPago.value = pagoSeleccionado.value;
        if (entregaSeleccionada) hiddenEntrega.value = entregaSeleccionada.value;

        // Habilitar botón solo si TODO está correcto
        if (pagoSeleccionado && entregaSeleccionada && direccionValida) {
            btnFinalizar.disabled = false;
            console.log("🟢 Botón habilitado");
        } else {
            btnFinalizar.disabled = true;
            console.log("🔴 Botón deshabilitado");
        }
    }

    // Mostrar/ocultar sección de dirección
    inputEntregas.forEach(opt => {
        opt.addEventListener("change", () => {
            if (opt.value === "despacho") {
                direccionBlock.classList.remove("hidden");
            } else {
                direccionBlock.classList.add("hidden");
            }
            validarTodo();
        });
    });

    // Opciones de dirección
    direccionOptions.forEach(opt => {
        opt.addEventListener("change", () => {
            if (opt.value === "nueva") {
                nuevaDireccionCampo.classList.remove("hidden");
            } else {
                nuevaDireccionCampo.classList.add("hidden");
            }
            validarTodo();
        });
    });

    // Validar cuando escribe nueva dirección
    if (inputNuevaDireccion) {
        inputNuevaDireccion.addEventListener("input", validarTodo);
    }

    // Validaciones principales
    inputPagos.forEach(inp => inp.addEventListener("change", validarTodo));
    inputEntregas.forEach(inp => inp.addEventListener("change", validarTodo));

});
