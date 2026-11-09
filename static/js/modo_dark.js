function aplicarTema() {
  const tieneTemaGuardado = "theme" in localStorage;
  const prefiereOscuro = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const esOscuro = localStorage.theme === "dark" || (!tieneTemaGuardado && prefiereOscuro);

  if (esOscuro) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  // Actualizar la interfaz del botón único si existe en el DOM
  actualizarBoton(esOscuro);
}

function alternarTema() {
  const tieneTemaGuardado = "theme" in localStorage;
  const prefiereOscuro = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const esOscuroActual = localStorage.theme === "dark" || (!tieneTemaGuardado && prefiereOscuro);

  // Al hacer clic, alterna al estado opuesto
  if (esOscuroActual) {
    localStorage.theme = "light";
  } else {
    localStorage.theme = "dark";
  }

  aplicarTema();
}

function actualizarBoton(esOscuro) {
  const icono = document.getElementById("icono-tema");
  const texto = document.getElementById("texto-tema");

  if (!icono || !texto) return;

  if (esOscuro) {
    icono.textContent = "🌙";
    texto.textContent = "Oscuro";
  } else {
    icono.textContent = "☀️";
    texto.textContent = "Claro";
  }
}

// 1. Aplicar tema inmediatamente al cargar el script
aplicarTema();

// 2. Sincronizar el botón una vez cargado el DOM
document.addEventListener("DOMContentLoaded", aplicarTema);

// 3. Escuchar cambios del sistema en tiempo real si no hay un tema guardado manualmente
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
  if (!("theme" in localStorage)) {
    aplicarTema();
  }
});