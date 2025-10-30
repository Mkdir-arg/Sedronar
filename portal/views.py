from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from core.models import Institucion, Provincia, Municipio, Localidad
from core.forms import InstitucionForm


class PortalHomeView(TemplateView):
    template_name = 'portal/home.html'


@csrf_exempt
def crear_usuario_institucion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'portal/crear_usuario.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False  # Deshabilitado hasta aprobación
        )
        
        grupo_institucion, _ = Group.objects.get_or_create(name='EncargadoInstitucion')
        user.groups.add(grupo_institucion)
        
        # Guardar ID del usuario en sesión para el registro de institución
        request.session['pending_user_id'] = user.id
        print(f"DEBUG: Usuario creado - ID: {user.id}, Username: {user.username}, Email: {user.email}")
        print(f"DEBUG: Guardado en sesión - pending_user_id: {user.id}")
        messages.success(request, 'Usuario creado exitosamente. Complete ahora los datos de su institución.')
        return redirect('portal:registro_institucion')
    
    return render(request, 'portal/crear_usuario.html')


@csrf_exempt
def registro_institucion(request):
    # Verificar si hay un usuario pendiente en sesión o si está autenticado
    pending_user_id = request.session.get('pending_user_id')
    print(f"DEBUG: Accediendo a registro institución")
    print(f"DEBUG: Usuario autenticado: {request.user.is_authenticated}")
    print(f"DEBUG: pending_user_id en sesión: {pending_user_id}")
    
    if not request.user.is_authenticated and not pending_user_id:
        print(f"DEBUG: Redirigiendo a crear usuario - no hay usuario ni sesión")
        return redirect('portal:crear_usuario')
    
    if request.method == 'POST':
        form = InstitucionForm(request.POST)
        if form.is_valid():
            institucion = form.save(commit=False)
            institucion.estado_registro = 'ENVIADO'
            institucion.save()
            
            # Asociar usuario (priorizar pendiente sobre autenticado)
            if pending_user_id:
                try:
                    pending_user = User.objects.get(id=pending_user_id)
                    print(f"DEBUG: Asociando usuario pendiente: {pending_user.username} (ID: {pending_user_id})")
                    institucion.encargados.add(pending_user)
                    print(f"DEBUG: Usuario pendiente asociado exitosamente")
                    # Limpiar sesión
                    del request.session['pending_user_id']
                except User.DoesNotExist:
                    print(f"DEBUG: Error - Usuario con ID {pending_user_id} no encontrado")
                    messages.error(request, 'Error: Usuario no encontrado')
                    return redirect('portal:crear_usuario')
            elif request.user.is_authenticated:
                print(f"DEBUG: Asociando usuario autenticado: {request.user.username}")
                institucion.encargados.add(request.user)
                print(f"DEBUG: Usuario asociado exitosamente")
            else:
                print(f"DEBUG: Error - No hay usuario autenticado ni pendiente en sesión")
            
            messages.success(request, 'Solicitud enviada correctamente. Recibirá notificaciones por email.')
            return redirect('portal:consultar_tramite')
    else:
        form = InstitucionForm()
    
    return render(request, 'portal/registro_institucion.html', {'form': form})


@csrf_exempt
def consultar_tramite(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(f"DEBUG: Buscando email: {email}")
        
        try:
            user = User.objects.get(email=email)
            print(f"DEBUG: Usuario encontrado: {user.username}")
            
            instituciones = Institucion.objects.filter(encargados=user)
            print(f"DEBUG: Instituciones encontradas: {instituciones.count()}")
            
            for inst in instituciones:
                print(f"DEBUG: - {inst.nombre} ({inst.estado_registro})")
            
            return render(request, 'portal/consultar_tramite.html', {
                'instituciones': instituciones,
                'email': email
            })
        except User.DoesNotExist:
            print(f"DEBUG: Usuario no encontrado con email: {email}")
            messages.error(request, 'No se encontraron trámites con ese email')
    
    return render(request, 'portal/consultar_tramite.html')


def get_municipios(request):
    provincia_id = request.GET.get('provincia_id')
    municipios = Municipio.objects.filter(provincia_id=provincia_id).values('id', 'nombre')
    return JsonResponse(list(municipios), safe=False)


def get_localidades(request):
    municipio_id = request.GET.get('municipio_id')
    localidades = Localidad.objects.filter(municipio_id=municipio_id).values('id', 'nombre')
    return JsonResponse(list(localidades), safe=False)