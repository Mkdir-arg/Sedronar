/**
 * Sistema de alertas para conversaciones (versión simple sin WebSocket)
 */

class AlertasConversacionesSimple {
    constructor() {
        this.pollingInterval = null;
        this.ultimoConteo = 0;
        this.init();
    }

    init() {
        // Solo inicializar si el usuario tiene rol de conversaciones
        if (!this.tieneRolConversaciones()) {
            return;
        }

        this.iniciarPolling();
        this.configurarEventos();
    }

    tieneRolConversaciones() {
        const userGroups = window.userGroups || [];
        return userGroups.includes('Conversaciones') || userGroups.includes('OperadorCharla');
    }

    iniciarPolling() {
        // Verificar inmediatamente
        this.verificarAlertas();
        
        // Polling cada 10 segundos
        this.pollingInterval = setInterval(() => {
            this.verificarAlertas();
        }, 10000);
    }

    async verificarAlertas() {
        try {
            const response = await fetch('/conversaciones/api/alertas/count/');
            if (!response.ok) return;
            
            const data = await response.json();
            const nuevoConteo = data.count || 0;
            
            // Si hay nuevos mensajes, actualizar UI
            if (nuevoConteo > this.ultimoConteo) {
                this.mostrarNuevaAlerta(nuevoConteo - this.ultimoConteo);
                this.reproducirSonido();
            }
            
            this.ultimoConteo = nuevoConteo;
            this.actualizarContadorUI(nuevoConteo);
            
            // Actualizar preview si el dropdown está abierto
            this.actualizarPreview();
            
        } catch (error) {
            console.error('Error verificando alertas:', error);
        }
    }

    actualizarContadorUI(count) {
        const contador = document.getElementById('alertas-counter');
        if (!contador) return;
        
        // Obtener contador actual del sistema principal
        const contadorActual = parseInt(contador.textContent) || 0;
        
        // Si hay alertas de conversaciones, sumarlas
        if (count > 0) {
            const nuevoTotal = contadorActual + count;
            contador.textContent = nuevoTotal;
            contador.classList.remove('hidden');
            contador.classList.add('animate-pulse');
        } else if (contadorActual === 0) {
            contador.classList.add('hidden');
            contador.classList.remove('animate-pulse');
        }
    }

    async actualizarPreview() {
        const preview = document.getElementById('alertas-preview');
        if (!preview) return;
        
        try {
            const response = await fetch('/conversaciones/api/alertas/preview/');
            if (!response.ok) return;
            
            const data = await response.json();
            const alertas = data.results || [];
            
            if (alertas.length > 0) {
                // Agregar alertas de conversaciones al preview existente
                const alertasHTML = alertas.map(alerta => `
                    <div class="p-3 border-b border-gray-100 hover:bg-gray-50 cursor-pointer" 
                         onclick="window.location.href='/conversaciones/${alerta.conversacion_id}/'">
                        <div class="flex items-start justify-between">
                            <div class="flex-1">
                                <p class="text-sm font-medium text-gray-900">
                                    <i class="fas fa-comment-dots mr-1 text-blue-500"></i>
                                    ${alerta.ciudadano_nombre}
                                </p>
                                <p class="text-xs text-gray-600 mt-1">${alerta.contenido}</p>
                                <p class="text-xs text-gray-400 mt-1">${alerta.fecha}</p>
                            </div>
                            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                MENSAJE
                            </span>
                        </div>
                    </div>
                `).join('');
                
                // Si el preview está vacío o solo tiene el mensaje de "no hay alertas"
                if (preview.innerHTML.includes('No hay alertas activas') || 
                    preview.innerHTML.includes('Cargando alertas')) {
                    preview.innerHTML = alertasHTML;
                } else {
                    // Agregar al inicio del preview existente
                    preview.innerHTML = alertasHTML + preview.innerHTML;
                }
            }
        } catch (error) {
            console.error('Error actualizando preview:', error);
        }
    }

    mostrarNuevaAlerta(cantidad) {
        // Toast notification
        this.mostrarToast(cantidad);
        
        // Notificación del navegador
        if (Notification.permission === 'granted') {
            new Notification('Nuevos mensajes en conversaciones', {
                body: `Tienes ${cantidad} mensaje(s) nuevo(s)`,
                icon: '/static/custom/img/logo.png'
            });
        }
    }

    mostrarToast(cantidad) {
        const toast = document.createElement('div');
        toast.className = 'fixed top-4 right-4 bg-blue-600 text-white px-4 py-3 rounded-lg shadow-lg z-50 max-w-sm animate-slide-in';
        toast.innerHTML = `
            <div class="flex items-start">
                <i class="fas fa-comment-dots mr-2 mt-1"></i>
                <div class="flex-1">
                    <div class="font-medium">Nuevos mensajes</div>
                    <div class="text-sm opacity-90">Tienes ${cantidad} mensaje(s) nuevo(s)</div>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    reproducirSonido() {
        try {
            if (window.notificationSound) {
                window.notificationSound.playDoubleBeep();
            }
        } catch (e) {
            console.warn('No se pudo reproducir sonido:', e);
        }
    }

    configurarEventos() {
        // Solicitar permisos de notificación
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
        
        // Limpiar contador cuando se hace clic en el dropdown
        const alertasDropdown = document.querySelector('[x-data*="showDropdown"]');
        if (alertasDropdown) {
            alertasDropdown.addEventListener('click', () => {
                setTimeout(() => {
                    this.marcarComoVisto();
                }, 1000);
            });
        }
    }

    async marcarComoVisto() {
        // Resetear contador local
        this.ultimoConteo = 0;
        
        // Actualizar UI
        const contador = document.getElementById('alertas-counter');
        if (contador) {
            contador.classList.add('hidden');
            contador.classList.remove('animate-pulse');
        }
    }

    destruir() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
        }
    }
}

// CSS para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slide-in {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    .animate-slide-in {
        animation: slide-in 0.3s ease-out;
    }
`;
document.head.appendChild(style);

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.alertasConversaciones = new AlertasConversacionesSimple();
});

// Limpiar al salir de la página
window.addEventListener('beforeunload', () => {
    if (window.alertasConversaciones) {
        window.alertasConversaciones.destruir();
    }
});