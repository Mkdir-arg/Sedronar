/**
 * Sistema de alertas para conversaciones
 * Maneja notificaciones en tiempo real para operadores con rol Conversaciones
 */

class AlertasConversaciones {
    constructor() {
        this.socket = null;
        this.alertasActivas = new Map();
        this.init();
    }

    init() {
        // Solo inicializar si el usuario tiene rol de conversaciones
        if (!this.tieneRolConversaciones()) {
            return;
        }

        this.conectarWebSocket();
        this.configurarEventos();
    }

    tieneRolConversaciones() {
        // Verificar si el usuario tiene permisos de conversaciones
        const userGroups = window.userGroups || [];
        return userGroups.includes('Conversaciones') || userGroups.includes('OperadorCharla');
    }

    conectarWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/alertas-conversaciones/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            console.log('Conectado a alertas de conversaciones');
            this.actualizarEstadoConexion(true);
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.manejarMensaje(data);
        };
        
        this.socket.onclose = () => {
            console.log('Desconectado de alertas de conversaciones');
            this.actualizarEstadoConexion(false);
            // Reconectar después de 3 segundos
            setTimeout(() => this.conectarWebSocket(), 3000);
        };
        
        this.socket.onerror = (error) => {
            console.error('Error en WebSocket de conversaciones:', error);
        };
    }

    manejarMensaje(data) {
        switch (data.type) {
            case 'nueva_alerta_conversacion':
                this.agregarAlerta(data.alerta);
                break;
        }
    }

    agregarAlerta(alerta) {
        // Agregar a la lista de alertas activas
        this.alertasActivas.set(alerta.id, alerta);
        
        // Integrar con el sistema de alertas existente
        this.integrarConSistemaExistente(alerta);
        
        // Mostrar notificación
        this.mostrarNotificacion(alerta);
        
        // Reproducir sonido si está habilitado
        this.reproducirSonido();
    }

    integrarConSistemaExistente(alerta) {
        // Actualizar el preview de alertas existente
        const preview = document.getElementById('alertas-preview');
        if (preview) {
            // Crear elemento de alerta para el dropdown
            const alertaElement = document.createElement('div');
            alertaElement.className = 'p-3 border-b border-gray-100 hover:bg-gray-50 cursor-pointer';
            alertaElement.innerHTML = `
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <p class="text-sm font-medium text-gray-900">Conversación #${alerta.conversacion_id}</p>
                        <p class="text-xs text-gray-600 mt-1">${alerta.contenido_mensaje}</p>
                        <p class="text-xs text-gray-400 mt-1">${alerta.fecha}</p>
                    </div>
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        MENSAJE
                    </span>
                </div>
            `;
            
            // Hacer clic para ir a la conversación
            alertaElement.addEventListener('click', () => {
                window.location.href = `/conversaciones/${alerta.conversacion_id}/`;
            });
            
            // Insertar al inicio del preview
            if (preview.innerHTML.includes('No hay alertas activas')) {
                preview.innerHTML = '';
            }
            preview.insertBefore(alertaElement, preview.firstChild);
        }
        
        // Actualizar contador
        this.actualizarContador();
    }
    
    actualizarContador() {
        const contador = document.getElementById('alertas-counter');
        const cantidad = this.alertasActivas.size;
        
        if (contador) {
            // Obtener contador actual y sumar las alertas de conversaciones
            const contadorActual = parseInt(contador.textContent) || 0;
            const nuevoTotal = contadorActual + cantidad;
            
            if (nuevoTotal > 0) {
                contador.textContent = nuevoTotal;
                contador.classList.remove('hidden');
                contador.classList.add('animate-pulse');
            } else {
                contador.classList.add('hidden');
                contador.classList.remove('animate-pulse');
            }
        }
    }

    mostrarNotificacion(alerta) {
        // Crear notificación del navegador si está permitido
        if (Notification.permission === 'granted') {
            new Notification('Nuevo mensaje en conversación', {
                body: alerta.contenido_mensaje,
                icon: '/static/custom/img/logo.png',
                tag: alerta.id
            });
        }
        
        // Mostrar toast interno
        this.mostrarToast(alerta);
    }

    mostrarToast(alerta) {
        const toast = document.createElement('div');
        toast.className = 'fixed top-4 right-4 bg-blue-600 text-white px-4 py-3 rounded-lg shadow-lg z-50 max-w-sm';
        toast.innerHTML = `
            <div class="flex items-start">
                <i class="fas fa-comment-dots mr-2 mt-1"></i>
                <div class="flex-1">
                    <div class="font-medium">Nuevo mensaje</div>
                    <div class="text-sm opacity-90">Conversación #${alerta.conversacion_id}</div>
                    <div class="text-xs opacity-75 mt-1">${alerta.contenido_mensaje}</div>
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
        
        // Hacer clic para ir a la conversación
        toast.addEventListener('click', () => {
            window.location.href = `/conversaciones/${alerta.conversacion_id}/`;
            toast.remove();
        });
    }

    reproducirSonido() {
        // Reproducir sonido de notificación
        try {
            if (window.notificationSound) {
                window.notificationSound.playDoubleBeep();
            }
        } catch (e) {
            // Fallar silenciosamente
        }
    }

    configurarEventos() {
        // Solicitar permisos de notificación
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
        
        // Limpiar alerta cuando se hace clic en el dropdown
        const alertasDropdown = document.querySelector('[x-data*="showDropdown"]');
        if (alertasDropdown) {
            alertasDropdown.addEventListener('click', () => {
                // Limpiar alertas después de un breve delay
                setTimeout(() => {
                    this.limpiarAlertas();
                }, 1000);
            });
        }
    }

    limpiarAlertas() {
        // Limpiar alertas activas
        this.alertasActivas.clear();
        
        // Actualizar contador sin las alertas de conversaciones
        const contador = document.getElementById('alertas-counter');
        if (contador && window.alertasWS) {
            // Dejar que el sistema principal actualice el contador
            window.alertasWS.updateAlertasCounter();
        }
    }

    actualizarEstadoConexion(conectado) {
        const indicador = document.getElementById('websocket-status');
        if (indicador) {
            if (conectado) {
                indicador.className = 'w-2 h-2 rounded-full bg-green-400';
                indicador.title = 'Conectado - Alertas activas';
            } else {
                indicador.className = 'w-2 h-2 rounded-full bg-red-400';
                indicador.title = 'Desconectado - Reconectando...';
            }
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.alertasConversaciones = new AlertasConversaciones();
});