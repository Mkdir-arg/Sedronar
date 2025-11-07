from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from core.models import Institucion
from legajos.models import LegajoAtencion


def es_staff(user):
    return user.is_superuser or user.is_staff or user.groups.filter(name__in=['Administrador', 'Supervisor']).exists()


@login_required
@user_passes_test(es_staff)
def lista_tramites(request):
    tramites = Institucion.objects.filter(
        estado_registro__in=['ENVIADO', 'REVISION']
    ).select_related('provincia', 'municipio', 'localidad').prefetch_related('encargados').order_by('-creado')
    
    # Debug: crear trámite de prueba si no hay ninguno
    if not tramites.exists():
        from core.models import Provincia, Municipio
        provincia = Provincia.objects.first()
        municipio = Municipio.objects.first()
        if provincia and municipio:
            Institucion.objects.create(
                tipo='DTC',
                nombre='Institución de Prueba',
                provincia=provincia,
                municipio=municipio,
                email='prueba@test.com',
                estado_registro='ENVIADO',
                descripcion='Trámite de prueba para testing'
            )
            tramites = Institucion.objects.filter(
                estado_registro__in=['ENVIADO', 'REVISION']
            ).select_related('provincia', 'municipio', 'localidad').prefetch_related('encargados').order_by('-creado')
    
    return render(request, 'tramites/lista_tramites.html', {
        'tramites': tramites
    })


@login_required
@user_passes_test(es_staff)
def detalle_tramite(request, tramite_id):
    tramite = get_object_or_404(Institucion, id=tramite_id)
    
    return render(request, 'tramites/detalle_tramite.html', {
        'tramite': tramite
    })


@login_required
@user_passes_test(es_staff)
def aprobar_tramite(request, tramite_id):
    if request.method == 'POST':
        tramite = get_object_or_404(Institucion, id=tramite_id)
        
        # Verificar si puede ser aprobado
        if not tramite.puede_aprobar:
            messages.error(request, f'El trámite ya está en estado {tramite.get_estado_registro_display()} y no puede ser aprobado.')
            return redirect('tramites:detalle_tramite', tramite_id=tramite_id)
        
        nro_registro = request.POST.get('nro_registro')
        resolucion = request.POST.get('resolucion')
        
        # Aprobar institución
        tramite.aprobar(nro_registro=nro_registro, resolucion=resolucion)
        
        # Crear ciudadano dummy para el legajo institucional
        from legajos.models import Ciudadano
        ciudadano_dummy, created = Ciudadano.objects.get_or_create(
            dni='00000000',
            defaults={
                'nombre': 'Institución',
                'apellido': tramite.nombre,
                'genero': 'X'
            }
        )
        
        # Crear legajo institucional
        legajo = LegajoAtencion.objects.create(
            dispositivo=tramite,
            responsable=request.user,
            ciudadano=ciudadano_dummy,
            notas=f'Legajo institucional creado automáticamente al aprobar registro {nro_registro}'
        )
        
        # Habilitar usuarios (optimizado)
        tramite.encargados.update(is_active=True)
        
        messages.success(request, f'Trámite aprobado. Legajo {legajo.codigo} creado.')
        return redirect('tramites:lista_tramites')
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
@user_passes_test(es_staff)
def rechazar_tramite(request, tramite_id):
    if request.method == 'POST':
        tramite = get_object_or_404(Institucion, id=tramite_id)
        motivo = request.POST.get('motivo')
        
        tramite.rechazar(motivo)
        
        messages.warning(request, 'Trámite rechazado.')
        return redirect('tramites:lista_tramites')
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)