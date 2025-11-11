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
        
        # Crear usuario para la institución
        from django.contrib.auth.models import User, Group
        username = f"institucion_{tramite.id}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': tramite.email,
                'first_name': tramite.nombre[:30],
                'is_active': True
            }
        )
        
        if created:
            # Asignar grupo EncargadoInstitucion
            grupo, _ = Group.objects.get_or_create(name='EncargadoInstitucion')
            user.groups.add(grupo)
            
            # Asociar usuario a la institución
            tramite.encargados.add(user)
        
        messages.success(request, f'Trámite aprobado. Usuario {username} creado.')
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