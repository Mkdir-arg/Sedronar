from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import LegajoAtencion, Ciudadano
from datetime import datetime
try:
    from .models_contactos import VinculoFamiliar
except ImportError:
    VinculoFamiliar = None

def red_contactos_simple(request, legajo_id):
    """Vista simple para red de contactos"""
    legajo = get_object_or_404(LegajoAtencion, id=legajo_id)
    
    context = {
        'legajo': legajo,
        'ciudadano': legajo.ciudadano,
    }
    
    return render(request, 'legajos/red_contactos_simple.html', context)



def dashboard_contactos_simple(request):
    """Dashboard simple de contactos"""
    context = {
        'titulo': 'Dashboard de Contactos',
    }
    
    return render(request, 'legajos/dashboard_contactos_simple.html', context)

def historial_contactos_simple(request, legajo_id):
    """Vista simple para historial de contactos"""
    legajo = get_object_or_404(LegajoAtencion, id=legajo_id)
    
    context = {
        'legajo': legajo,
        'ciudadano': legajo.ciudadano,
    }
    
    return render(request, 'legajos/historial_contactos_simple.html', context)

def actividades_ciudadano_api(request, ciudadano_id):
    """API para obtener todas las actividades de un ciudadano"""
    try:
        ciudadano = get_object_or_404(Ciudadano, id=ciudadano_id)
        legajos = LegajoAtencion.objects.filter(ciudadano=ciudadano)
        
        actividades = []
        
        # Actividades básicas de legajos
        for legajo in legajos:
            # Apertura de legajo
            if legajo.fecha_apertura:
                actividades.append({
                    'fecha_hora': legajo.fecha_apertura.isoformat(),
                    'tipo': 'APERTURA',
                    'tipo_display': 'Apertura de Legajo',
                    'descripcion': f'Legajo abierto en {legajo.dispositivo.nombre if legajo.dispositivo else "Dispositivo no especificado"}',
                    'usuario_nombre': legajo.responsable.get_full_name() if legajo.responsable else 'Sistema',
                    'legajo_id': str(legajo.id),
                    'legajo_codigo': str(legajo.codigo)[:12] + '...' if legajo.codigo else str(legajo.id)
                })
            
            # Cierre de legajo
            if hasattr(legajo, 'fecha_cierre') and legajo.fecha_cierre:
                actividades.append({
                    'fecha_hora': legajo.fecha_cierre.isoformat(),
                    'tipo': 'CIERRE',
                    'tipo_display': 'Cierre de Legajo',
                    'descripcion': 'Legajo cerrado',
                    'usuario_nombre': 'Sistema',
                    'legajo_id': str(legajo.id),
                    'legajo_codigo': str(legajo.codigo)[:12] + '...' if legajo.codigo else str(legajo.id)
                })
        
        # Vínculos familiares
        try:
            vinculos = VinculoFamiliar.objects.filter(ciudadano_principal=ciudadano)
            for vinculo in vinculos:
                actividades.append({
                    'fecha_hora': vinculo.creado.isoformat() if hasattr(vinculo, 'creado') else datetime.now().isoformat(),
                    'tipo': 'VINCULO',
                    'tipo_display': 'Vínculo Familiar',
                    'descripcion': f'Vínculo agregado: {vinculo.get_tipo_vinculo_display() if hasattr(vinculo, "get_tipo_vinculo_display") else vinculo.tipo_vinculo}',
                    'usuario_nombre': 'Sistema',
                    'legajo_id': '-',
                    'legajo_codigo': 'General'
                })
        except Exception as e:
            print(f"Error cargando vínculos: {e}")
        
        # Ordenar por fecha descendente
        actividades.sort(key=lambda x: x['fecha_hora'] or '', reverse=True)
        
        return JsonResponse({
            'results': actividades[:20],  # Limitar a 20 registros
            'count': len(actividades)
        })
        
    except Exception as e:
        print(f"Error en actividades_ciudadano_api: {e}")
        return JsonResponse({
            'results': [],
            'count': 0,
            'error': str(e)
        })

def subir_archivos_legajo(request, legajo_id):
    """Vista para subir archivos a un legajo"""
    if request.method == 'POST':
        try:
            legajo = get_object_or_404(LegajoAtencion, id=legajo_id)
            
            archivos = request.FILES.getlist('archivo')
            etiqueta = request.POST.get('etiqueta', '')
            
            if not archivos:
                return JsonResponse({'success': False, 'error': 'No se seleccionaron archivos'})
            
            archivos_subidos = []
            
            for archivo in archivos:
                # Validar tamaño (10MB máximo)
                if archivo.size > 10 * 1024 * 1024:
                    return JsonResponse({'success': False, 'error': f'El archivo {archivo.name} es muy grande (máx. 10MB)'})
                
                # Validar extensión
                extensiones_permitidas = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
                nombre_archivo = archivo.name.lower()
                if not any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas):
                    return JsonResponse({'success': False, 'error': f'Formato no permitido: {archivo.name}'})
                
                # Crear adjunto usando el modelo genérico
                from django.contrib.contenttypes.models import ContentType
                from .models import Adjunto
                
                content_type = ContentType.objects.get_for_model(LegajoAtencion)
                adjunto = Adjunto.objects.create(
                    content_type=content_type,
                    object_id=legajo.id,
                    archivo=archivo,
                    etiqueta=etiqueta or archivo.name
                )
                
                archivos_subidos.append({
                    'id': adjunto.id,
                    'nombre': archivo.name,
                    'etiqueta': adjunto.etiqueta
                })
            
            return JsonResponse({
                'success': True,
                'archivos': archivos_subidos,
                'mensaje': f'{len(archivos_subidos)} archivo(s) subido(s) exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def archivos_ciudadano_api(request, ciudadano_id):
    """API para obtener todos los archivos de un ciudadano"""
    try:
        ciudadano = get_object_or_404(Ciudadano, id=ciudadano_id)
        legajos = LegajoAtencion.objects.filter(ciudadano=ciudadano)
        
        from django.contrib.contenttypes.models import ContentType
        from .models import Adjunto
        
        content_type = ContentType.objects.get_for_model(LegajoAtencion)
        archivos = Adjunto.objects.filter(
            content_type=content_type,
            object_id__in=[str(legajo.id) for legajo in legajos]
        ).order_by('-creado')
        
        archivos_data = []
        for archivo in archivos:
            legajo = LegajoAtencion.objects.get(id=archivo.object_id)
            archivos_data.append({
                'id': archivo.id,
                'nombre': archivo.archivo.name.split('/')[-1],
                'etiqueta': archivo.etiqueta,
                'url': archivo.archivo.url,
                'tamano': archivo.archivo.size,
                'fecha_subida': archivo.creado.isoformat(),
                'legajo_id': str(legajo.id),
                'legajo_codigo': str(legajo.codigo)[:12] + '...' if legajo.codigo else str(legajo.id)
            })
        
        return JsonResponse({
            'results': archivos_data,
            'count': len(archivos_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'results': [],
            'count': 0,
            'error': str(e)
        })

def eliminar_archivo(request, archivo_id):
    """Vista para eliminar un archivo"""
    if request.method == 'DELETE':
        try:
            from .models import Adjunto
            archivo = get_object_or_404(Adjunto, id=archivo_id)
            archivo.delete()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def alertas_ciudadano_api(request, ciudadano_id):
    """API para obtener alertas de un ciudadano"""
    try:
        from .services_alertas import AlertasService
        
        # Generar alertas actualizadas
        AlertasService.generar_alertas_ciudadano(ciudadano_id)
        
        # Obtener alertas activas
        alertas = AlertasService.obtener_alertas_ciudadano(ciudadano_id)
        
        alertas_data = []
        for alerta in alertas:
            alertas_data.append({
                'id': alerta.id,
                'tipo': alerta.tipo,
                'tipo_display': alerta.get_tipo_display(),
                'prioridad': alerta.prioridad,
                'mensaje': alerta.mensaje,
                'color_css': alerta.color_css,
                'fecha_creacion': alerta.creado.isoformat(),
                'legajo_id': str(alerta.legajo.id) if alerta.legajo else None
            })
        
        return JsonResponse({
            'results': alertas_data,
            'count': len(alertas_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'results': [],
            'count': 0,
            'error': str(e)
        })

def cerrar_alerta_api(request, alerta_id):
    """API para cerrar una alerta"""
    if request.method == 'POST':
        try:
            from .services_alertas import AlertasService
            
            success = AlertasService.cerrar_alerta(alerta_id, request.user)
            
            if success:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Alerta no encontrada'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})