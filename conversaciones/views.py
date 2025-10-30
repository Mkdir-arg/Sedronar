from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib import messages
from django.db import models
from .models import Conversacion, Mensaje
import json


# Vista pública para ciudadanos
def chat_ciudadano(request):
    return render(request, 'conversaciones/chat_ciudadano.html')


@csrf_exempt
def consultar_renaper(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dni = data.get('dni', '').strip()
        sexo = data.get('sexo', '').strip()
        
        if not dni or not sexo:
            return JsonResponse({'success': False, 'error': 'DNI y sexo son requeridos'})
        
        try:
            from legajos.services.consulta_renaper import consultar_datos_renaper
            resultado = consultar_datos_renaper(dni, sexo)
            
            if resultado['success']:
                datos = resultado['data']
                return JsonResponse({
                    'success': True,
                    'datos': {
                        'nombre': datos.get('nombre', ''),
                        'apellido': datos.get('apellido', ''),
                        'fecha_nacimiento': datos.get('fecha_nacimiento', ''),
                        'domicilio': datos.get('domicilio', '')
                    }
                })
            else:
                # Si RENAPER falla o persona fallecida
                if resultado.get('fallecido'):
                    return JsonResponse({
                        'success': False, 
                        'error': 'La persona consultada figura como fallecida en RENAPER'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': resultado.get('error', 'Error al consultar RENAPER')
                    })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error interno al consultar datos: {str(e)}'
            })
    
    return JsonResponse({'success': False})


@csrf_exempt
def iniciar_conversacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo = data.get('tipo', 'anonima')
            dni = data.get('dni', '')
            sexo = data.get('sexo', '')
            datos_renaper = data.get('datos_renaper', {})
            prioridad = data.get('prioridad', 'normal')
            
            conversacion = Conversacion.objects.create(
                tipo=tipo,
                dni_ciudadano=dni if tipo == 'personal' and dni else None,
                sexo_ciudadano=sexo if tipo == 'personal' and sexo else None,
                prioridad=prioridad,
                estado='activa'  # Iniciar como activa para que pueda ser asignada
            )
            
            print(f"DEBUG: Conversación creada - ID: {conversacion.id}, Tipo: {tipo}, Estado: {conversacion.estado}")
            
            # Solo crear ciudadano si es conversación personal y tenemos datos
            if tipo == 'personal' and dni and sexo:
                try:
                    from legajos.models import Ciudadano
                    ciudadano, created = Ciudadano.objects.get_or_create(
                        dni=dni,
                        defaults={
                            'nombre': datos_renaper.get('nombre', 'Usuario'),
                            'apellido': datos_renaper.get('apellido', 'Chat'),
                            'genero': sexo,
                            'domicilio': datos_renaper.get('domicilio', '')
                        }
                    )
                except Exception:
                    pass  # Si falla crear ciudadano, continuar con la conversación
            
            # Intentar asignación automática
            from .services import AsignadorAutomatico, NotificacionService
            
            asignado = AsignadorAutomatico.asignar_conversacion_automatica(conversacion)
            if asignado:
                conversacion.refresh_from_db()
            
            # Notificar nueva conversación
            NotificacionService.notificar_nueva_conversacion(conversacion)
            
            return JsonResponse({
                'success': True,
                'conversacion_id': conversacion.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al crear conversación: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@csrf_exempt
def enviar_mensaje_ciudadano(request, conversacion_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contenido = data.get('mensaje', '').strip()
            
            if not contenido:
                return JsonResponse({'success': False, 'error': 'Mensaje vacío'})
            
            conversacion = get_object_or_404(Conversacion, id=conversacion_id)
            
            mensaje = Mensaje.objects.create(
                conversacion=conversacion,
                remitente='ciudadano',
                contenido=contenido
            )
            
            print(f"DEBUG: Mensaje creado - ID: {mensaje.id}, Conversación: {conversacion_id}, Contenido: {contenido}")
        except Exception as e:
            print(f"DEBUG: Error al crear mensaje: {str(e)}")
            return JsonResponse({'success': False, 'error': f'Error interno: {str(e)}'})
        
        # TODO: Notificar nuevo mensaje via WebSocket cuando channels esté funcionando
        # from channels.layers import get_channel_layer
        # from asgiref.sync import async_to_sync
        # 
        # channel_layer = get_channel_layer()
        # 
        # # Notificar en la conversación específica
        # async_to_sync(channel_layer.group_send)(
        #     f'conversacion_{conversacion_id}',
        #     {
        #         'type': 'chat_message',
        #         'mensaje': {
        #             'id': mensaje.id,
        #             'contenido': mensaje.contenido,
        #             'remitente': 'ciudadano',
        #             'fecha': mensaje.fecha_envio.strftime('%H:%M'),
        #             'usuario': 'Ciudadano'
        #         }
        #     }
        # )
        # 
        # # Notificar en la lista de conversaciones
        # async_to_sync(channel_layer.group_send)(
        #     'conversaciones_list',
        #     {
        #         'type': 'nuevo_mensaje',
        #         'conversacion_id': conversacion_id,
        #         'mensaje': {
        #             'contenido': contenido[:50] + '...' if len(contenido) > 50 else contenido,
        #             'remitente': 'ciudadano'
        #         }
        #     }
        # )
        
        return JsonResponse({
            'success': True,
            'mensaje': {
                'id': mensaje.id,
                'contenido': mensaje.contenido,
                'fecha': mensaje.fecha_envio.strftime('%H:%M')
            }
        })
    
    return JsonResponse({'success': False})


@csrf_exempt
def obtener_mensajes_ciudadano(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    mensajes = conversacion.mensajes.all()
    
    print(f"DEBUG: Obteniendo mensajes para conversación {conversacion_id} - Total: {mensajes.count()}")
    
    mensajes_data = [{
        'id': msg.id,
        'remitente': msg.remitente,
        'contenido': msg.contenido,
        'fecha': msg.fecha_envio.strftime('%H:%M')
    } for msg in mensajes]
    
    return JsonResponse({'mensajes': mensajes_data})


# Vistas del backoffice
def tiene_permiso_conversaciones(user):
    return user.groups.filter(name__in=['Conversaciones', 'OperadorCharla']).exists() or user.is_superuser


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def lista_conversaciones(request):
    from datetime import datetime
    from django.db.models import Count, Q
    from django.contrib.auth.models import User
    
    # Filtros
    estado_filtro = request.GET.get('estado', '')
    operador_filtro = request.GET.get('operador', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    busqueda = request.GET.get('busqueda', '')
    tipo_filtro = request.GET.get('tipo', '')
    
    # Base queryset
    if request.user.groups.filter(name='OperadorCharla').exists() and not request.user.is_superuser:
        conversaciones = Conversacion.objects.select_related('operador_asignado').prefetch_related('mensajes').filter(
            models.Q(operador_asignado=None) | models.Q(operador_asignado=request.user)
        )
    else:
        conversaciones = Conversacion.objects.select_related('operador_asignado').prefetch_related('mensajes')
    
    # Aplicar filtros
    if estado_filtro:
        conversaciones = conversaciones.filter(estado=estado_filtro)
    
    if operador_filtro:
        if operador_filtro == 'sin_asignar':
            conversaciones = conversaciones.filter(operador_asignado=None)
        else:
            conversaciones = conversaciones.filter(operador_asignado_id=operador_filtro)
    
    if fecha_desde:
        conversaciones = conversaciones.filter(fecha_inicio__date__gte=fecha_desde)
    
    if fecha_hasta:
        conversaciones = conversaciones.filter(fecha_inicio__date__lte=fecha_hasta)
    
    if busqueda:
        conversaciones = conversaciones.filter(
            Q(id__icontains=busqueda) | Q(dni_ciudadano__icontains=busqueda)
        )
    
    if tipo_filtro:
        conversaciones = conversaciones.filter(tipo=tipo_filtro)
    
    # Estadísticas
    chats_no_atendidos = Conversacion.objects.filter(operador_asignado=None, estado='activa').count()
    
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    atendidos_mes = Conversacion.objects.filter(
        operador_asignado__isnull=False,
        fecha_inicio__month=mes_actual,
        fecha_inicio__year=año_actual
    ).count()
    
    tiempo_promedio = 0
    conversaciones_con_respuesta = Conversacion.objects.filter(
        operador_asignado__isnull=False,
        mensajes__remitente='operador'
    ).distinct()
    
    if conversaciones_con_respuesta.exists():
        tiempos = []
        for conv in conversaciones_con_respuesta:
            primer_msg_ciudadano = conv.mensajes.filter(remitente='ciudadano').first()
            primer_msg_operador = conv.mensajes.filter(remitente='operador').first()
            if primer_msg_ciudadano and primer_msg_operador:
                diff = primer_msg_operador.fecha_envio - primer_msg_ciudadano.fecha_envio
                tiempos.append(diff.total_seconds() / 60)
        
        if tiempos:
            tiempo_promedio = sum(tiempos) / len(tiempos)
    
    # Carga de trabajo por operador
    operadores_con_carga = User.objects.filter(
        groups__name__in=['Conversaciones', 'OperadorCharla']
    ).annotate(
        conversaciones_activas=Count('conversacion', filter=Q(conversacion__estado='activa'))
    ).order_by('first_name', 'last_name')
    
    # Todos los operadores para el filtro
    todos_operadores = User.objects.filter(
        groups__name__in=['Conversaciones', 'OperadorCharla']
    ).order_by('first_name', 'last_name')
    
    es_operador_charla = request.user.groups.filter(name='OperadorCharla').exists()
    
    for conversacion in conversaciones:
        conversacion.mensajes_no_leidos = conversacion.mensajes.filter(remitente='ciudadano', leido=False).count()
    
    return render(request, 'conversaciones/lista.html', {
        'conversaciones': conversaciones,
        'es_operador_charla': es_operador_charla,
        'chats_no_atendidos': chats_no_atendidos,
        'atendidos_mes': atendidos_mes,
        'tiempo_promedio': round(tiempo_promedio, 1),
        'operadores_con_carga': operadores_con_carga,
        'todos_operadores': todos_operadores,
        'filtros': {
            'estado': estado_filtro,
            'operador': operador_filtro,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'busqueda': busqueda,
            'tipo': tipo_filtro,
        }
    })


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def detalle_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    mensajes = conversacion.mensajes.all()
    
    # Marcar mensajes del ciudadano como leídos
    mensajes.filter(remitente='ciudadano', leido=False).update(leido=True)
    
    return render(request, 'conversaciones/detalle.html', {
        'conversacion': conversacion,
        'mensajes': mensajes
    })


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def asignar_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id, estado='activa')
    
    if request.method == 'POST':
        operador_id = request.POST.get('operador_id')
        if operador_id:
            from django.contrib.auth.models import User
            operador = get_object_or_404(User, id=operador_id)
            
            # Usar el método asignar_operador del modelo
            conversacion.asignar_operador(operador, request.user)
            
            messages.success(request, f'Conversación asignada a {operador.get_full_name()} exitosamente.')
        else:
            # Auto-asignación al usuario actual
            conversacion.asignar_operador(request.user, request.user)
            messages.success(request, 'Conversación asignada exitosamente.')
        
        # Actualizar colas después de la asignación
        from .services import AsignadorAutomatico
        AsignadorAutomatico.actualizar_todas_las_colas()
    
    return redirect('conversaciones:lista')


@login_required
@user_passes_test(tiene_permiso_conversaciones)
@csrf_exempt
def enviar_mensaje_operador(request, conversacion_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        contenido = data.get('mensaje', '').strip()
        
        if not contenido:
            return JsonResponse({'success': False, 'error': 'Mensaje vacío'})
        
        conversacion = get_object_or_404(Conversacion, id=conversacion_id)
        
        # Verificar que el operador puede responder
        if conversacion.operador_asignado and conversacion.operador_asignado != request.user:
            return JsonResponse({'success': False, 'error': 'No tienes permisos para responder esta conversación'})
        
        # Asignar operador si no tiene
        if not conversacion.operador_asignado:
            conversacion.operador_asignado = request.user
            conversacion.save()
        
        mensaje = Mensaje.objects.create(
            conversacion=conversacion,
            remitente='operador',
            contenido=contenido
        )
        
        # Marcar primera respuesta si es la primera
        conversacion.marcar_primera_respuesta()
        
        # Notificar mensaje
        from .services import NotificacionService
        NotificacionService.notificar_mensaje(conversacion, mensaje)
        
        return JsonResponse({
            'success': True,
            'mensaje': {
                'id': mensaje.id,
                'contenido': mensaje.contenido,
                'fecha': mensaje.fecha_envio.strftime('%H:%M')
            }
        })
    
    return JsonResponse({'success': False})


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def cerrar_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    conversacion.estado = 'cerrada'
    conversacion.fecha_cierre = timezone.now()
    conversacion.save()
    
    messages.success(request, 'Conversación cerrada exitosamente.')
    return redirect('conversaciones:lista')


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def reasignar_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id, estado='activa')
    
    if request.method == 'POST':
        operador_id = request.POST.get('operador_id')
        if operador_id:
            from django.contrib.auth.models import User
            operador = get_object_or_404(User, id=operador_id)
            
            conversacion.asignar_operador(operador, request.user)
            
            # Actualizar colas
            from .services import AsignadorAutomatico
            AsignadorAutomatico.actualizar_todas_las_colas()
            
            messages.success(request, f'Conversación reasignada a {operador.get_full_name()} exitosamente.')
    
    return redirect('conversaciones:lista')


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def metricas_conversaciones(request):
    """Vista de métricas del sistema de conversaciones"""
    from .services import MetricasService
    from .models import ColaAsignacion, MetricasOperador
    
    # Métricas globales
    metricas_globales = MetricasService.calcular_metricas_globales()
    
    # Métricas por operador
    metricas_operadores = MetricasOperador.objects.select_related('operador').all()
    
    # Estado de colas
    colas = ColaAsignacion.objects.select_related('operador').all()
    
    return render(request, 'conversaciones/metricas.html', {
        'metricas_globales': metricas_globales,
        'metricas_operadores': metricas_operadores,
        'colas': colas
    })


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def configurar_cola(request):
    """Vista para configurar la cola de asignación"""
    from .models import ColaAsignacion
    from .services import AsignadorAutomatico
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        operador_id = request.POST.get('operador_id')
        max_conversaciones = int(request.POST.get('max_conversaciones', 5))
        activo = request.POST.get('activo') == 'on'
        
        if operador_id:
            operador = get_object_or_404(User, id=operador_id)
            AsignadorAutomatico.configurar_operador(operador, max_conversaciones, activo)
            messages.success(request, f'Configuración actualizada para {operador.get_full_name()}')
    
    # Obtener operadores con permisos de conversaciones
    operadores = User.objects.filter(
        groups__name__in=['Conversaciones', 'OperadorCharla']
    ).order_by('first_name', 'last_name')
    
    colas = ColaAsignacion.objects.select_related('operador').all()
    
    return render(request, 'conversaciones/configurar_cola.html', {
        'operadores': operadores,
        'colas': colas
    })


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def asignacion_automatica(request):
    """Vista para forzar asignación automática de conversaciones sin asignar (solo a operadores logueados)"""
    from .services import AsignadorAutomatico
    
    # Buscar conversaciones activas sin operador asignado
    conversaciones_sin_asignar = Conversacion.objects.filter(
        estado='activa',
        operador_asignado=None
    )
    
    asignadas = 0
    sin_operadores = 0
    
    for conversacion in conversaciones_sin_asignar:
        if AsignadorAutomatico.asignar_conversacion_automatica(conversacion):
            asignadas += 1
        else:
            sin_operadores += 1
    
    # Actualizar todas las colas
    AsignadorAutomatico.actualizar_todas_las_colas()
    
    if asignadas > 0:
        messages.success(request, f'{asignadas} conversaciones asignadas automáticamente a operadores logueados')
    
    if sin_operadores > 0:
        messages.warning(request, f'{sin_operadores} conversaciones no pudieron asignarse (no hay operadores logueados disponibles)')
    
    if asignadas == 0 and sin_operadores == 0:
        messages.info(request, 'No hay conversaciones sin asignar')
    
    return redirect('conversaciones:lista')


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def evaluar_conversacion(request, conversacion_id):
    """Vista para que el ciudadano evalúe la conversación"""
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    
    if request.method == 'POST':
        satisfaccion = request.POST.get('satisfaccion')
        if satisfaccion:
            conversacion.satisfaccion = int(satisfaccion)
            conversacion.save()
            
            # Actualizar métricas del operador
            if conversacion.operador_asignado:
                from .services import MetricasService
                MetricasService.actualizar_metricas_operador(conversacion.operador_asignado)
            
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})


@login_required
@user_passes_test(tiene_permiso_conversaciones)
def api_metricas_tiempo_real(request):
    """API para obtener métricas en tiempo real"""
    from .services import MetricasService
    
    metricas = MetricasService.calcular_metricas_globales()
    
    return JsonResponse({
        'success': True,
        'metricas': metricas
    })