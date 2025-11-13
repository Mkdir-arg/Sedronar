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
    tramites_activos = Institucion.objects.filter(
        estado_registro__in=['ENVIADO', 'REVISION']
    ).select_related('provincia', 'municipio', 'localidad').prefetch_related('encargados').order_by('-creado')
    
    tramites_cerrados = Institucion.objects.filter(
        estado_registro__in=['APROBADO', 'RECHAZADO']
    ).select_related('provincia', 'municipio', 'localidad').prefetch_related('encargados').order_by('-modificado')
    
    return render(request, 'tramites/lista_tramites.html', {
        'tramites_activos': tramites_activos,
        'tramites_cerrados': tramites_cerrados
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
        
        # Activar usuario existente asociado a la institución
        from django.contrib.auth.models import User, Group
        usuario_existente = tramite.encargados.first()
        
        if usuario_existente:
            # Activar el usuario que se registró desde el portal
            usuario_existente.is_active = True
            usuario_existente.save()
            messages.success(request, f'Trámite aprobado. Usuario {usuario_existente.username} activado.')
        else:
            # Si no hay usuario asociado, crear uno nuevo (caso excepcional)
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
                grupo, _ = Group.objects.get_or_create(name='EncargadoInstitucion')
                user.groups.add(grupo)
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