// Configuración global de la aplicación
document.addEventListener('DOMContentLoaded', () => {
    console.log("Sistema cargado exitosamente.");
    
    // Inicializar iconos de Lucide en toda la página
    if (window.lucide) {
        lucide.createIcons();
    }
});

/**
 * Función global para mostrar alertas de error (útil para image_1c3d98.png)
 * @param {string} mensaje - El texto a mostrar
 * @param {string} elementoId - ID del contenedor del error
 */
function mostrarError(mensaje, elementoId = 'error-msg') {
    const errorBox = document.getElementById(elementoId);
    if (errorBox) {
        errorBox.textContent = mensaje;
        errorBox.classList.remove('d-none');
        
        // Ocultar automáticamente después de 5 segundos
        setTimeout(() => {
            errorBox.classList.add('d-none');
        }, 5000);
    } else {
        alert(mensaje);
    }
}

/**
 * Helper para peticiones fetch con JSON
 */
async function apiFetch(url, options = {}) {
    const defaultOptions = {
        headers: { 'Content-Type': 'application/json' }
    };
    
    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        return await response.json();
    } catch (error) {
        console.error("Error en la petición:", error);
        throw error;
    }
}