// WebSocket global para lista de conversaciones (sin recargar la página)
(function() {
    function incChatsNoAtendidos(delta) {
        const el = document.querySelector('[data-stat="chats-no-atendidos"]');
        if (!el) return;
        const actual = parseInt(el.textContent) || 0;
        const nuevo = actual + delta;
        el.textContent = nuevo;
        el.style.backgroundColor = '#fef3c7';
        setTimeout(() => el.style.backgroundColor = '', 1200);
    }

    function notificar(mensaje) {
        const prev = document.querySelectorAll('.notif-conv-lista');
        prev.forEach(n => n.remove());
        const n = document.createElement('div');
        n.className = 'notif-conv-lista fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white bg-green-600';
        n.innerHTML = `<div class="flex items-center"><span>${mensaje}</span><button class="ml-3" aria-label="Cerrar">✕</button></div>`;
        n.querySelector('button').addEventListener('click', () => n.remove());
        document.body.appendChild(n);
        setTimeout(() => { if (n.parentElement) n.remove(); }, 4000);
    }

    function agregarFilaDesktop(conv) {
        const tbody = document.querySelector('table tbody');
        if (!tbody) return;
        // Evitar duplicados
        if (document.querySelector(`tr[data-conversacion-id="${conv.id}"]`)) return;
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-gray-50';
        tr.setAttribute('data-conversacion-id', conv.id);
        const tipoBadge = (conv.tipo && String(conv.tipo).toLowerCase() === 'personal') ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800';
        const estadoBadge = (conv.estado === 'activa') ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800';
        tr.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#${conv.id}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${tipoBadge}">${conv.tipo || ''}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${conv.dni || '-'} ${conv.sexo ? `<span class="text-xs text-gray-500">(${conv.sexo})</span>` : ''}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${estadoBadge}">${conv.estado_display || conv.estado || ''}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${conv.operador || 'Sin asignar'}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${conv.fecha || ''}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">${conv.mensajes || 0}</span>
                ${conv.no_leidos && conv.no_leidos > 0 ? `<span class="contador-mensajes ml-1 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">${conv.no_leidos} sin leer</span>` : ''}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2">
                    <a href="/conversaciones/${conv.id}/" class="text-blue-600 hover:text-blue-900"><i class="fas fa-eye"></i> Ver</a>
                </div>
            </td>
        `;
        tbody.prepend(tr);
    }

    async function cargarYAgregarConversacion(conversacionId) {
        try {
            const r = await fetch(`/conversaciones/api/conversacion/${conversacionId}/`);
            if (!r.ok) return;
            const data = await r.json();
            if (data && data.conversacion) {
                agregarFilaDesktop(data.conversacion);
            }
        } catch (_) {}
    }

    function conectarWS() {
        if (window.conversacionesListaWS && window.conversacionesListaWS.readyState === 1) return;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/conversaciones/`;
        const ws = new WebSocket(wsUrl);
        window.conversacionesListaWS = ws;

        ws.onopen = () => {
            // console.log('[Conversaciones Lista] WS conectado');
        };
        ws.onmessage = (ev) => {
            try {
                const data = JSON.parse(ev.data);
                if (data.type === 'nueva_conversacion') {
                    incChatsNoAtendidos(1);
                    const msg = data.mensaje || 'Nueva conversación disponible';
                    notificar(msg);
                    let convId = data.conversacion_id;
                    if (!convId && typeof data.mensaje === 'string') {
                        const m = data.mensaje.match(/#(\d+)/);
                        if (m) convId = parseInt(m[1], 10);
                    }
                    if (convId && document.querySelector('table tbody')) {
                        cargarYAgregarConversacion(convId);
                    }
                } else if (data.type === 'nuevo_mensaje') {
                    const fila = document.querySelector(`tr[data-conversacion-id="${data.conversacion_id}"]`);
                    if (fila) {
                        const badge = fila.querySelector('.contador-mensajes');
                        if (badge) {
                            const v = parseInt(badge.textContent) || 0;
                            badge.textContent = v + 1;
                            badge.classList.add('animate-pulse');
                            setTimeout(() => badge.classList.remove('animate-pulse'), 800);
                        }
                    }
                }
            } catch (_) {}
        };
        ws.onclose = () => setTimeout(conectarWS, 3000);
        ws.onerror = () => {};
    }

    document.addEventListener('DOMContentLoaded', () => {
        conectarWS();
    });
})();

