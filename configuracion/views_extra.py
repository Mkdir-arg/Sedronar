from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from legajos.models import PlanFortalecimiento


class InscriptoEditarView(LoginRequiredMixin, UpdateView):
    model = None
    template_name = 'configuracion/inscripto_form.html'
    
    def get_object(self):
        from legajos.models import InscriptoActividad
        return get_object_or_404(InscriptoActividad, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inscripto'] = self.get_object()
        return context
    
    def post(self, request, *args, **kwargs):
        from legajos.models import InscriptoActividad, HistorialInscripto
        from django.utils import timezone
        from django.contrib import messages
        
        inscripto = self.get_object()
        nuevo_estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones', '')
        
        if nuevo_estado and nuevo_estado != inscripto.estado:
            estado_anterior = inscripto.estado
            inscripto.estado = nuevo_estado
            
            if nuevo_estado in ['FINALIZADO', 'ABANDONADO']:
                inscripto.fecha_finalizacion = timezone.now().date()
            
            inscripto.observaciones = observaciones
            inscripto.save()
            
            accion_map = {
                'FINALIZADO': 'FINALIZACION',
                'ABANDONADO': 'ABANDONO',
                'ACTIVO': 'ACTIVACION'
            }
            
            HistorialInscripto.objects.create(
                inscripto=inscripto,
                accion=accion_map.get(nuevo_estado, 'INSCRIPCION'),
                usuario=request.user,
                descripcion=f'Estado cambiado a {inscripto.get_estado_display()}. {observaciones}',
                estado_anterior=estado_anterior
            )
            
            messages.success(request, f'Estado del inscripto actualizado a {inscripto.get_estado_display()}')
        
        return redirect('configuracion:actividad_detalle', pk=inscripto.actividad.pk)


class ActividadEditarView(LoginRequiredMixin, UpdateView):
    model = PlanFortalecimiento
    fields = ['nombre', 'descripcion', 'cupo_ciudadanos', 'fecha_inicio', 'fecha_fin', 'estado']
    template_name = 'configuracion/actividad_editar_form.html'
    
    def form_valid(self, form):
        from legajos.models import HistorialActividad
        from django.contrib import messages
        
        actividad_anterior = PlanFortalecimiento.objects.get(pk=self.object.pk)
        cambios = []
        
        if actividad_anterior.nombre != form.cleaned_data['nombre']:
            cambios.append(f"Nombre: '{actividad_anterior.nombre}' → '{form.cleaned_data['nombre']}'")
        if actividad_anterior.cupo_ciudadanos != form.cleaned_data['cupo_ciudadanos']:
            cambios.append(f"Cupo: {actividad_anterior.cupo_ciudadanos} → {form.cleaned_data['cupo_ciudadanos']}")
        if actividad_anterior.estado != form.cleaned_data['estado']:
            cambios.append(f"Estado: {actividad_anterior.get_estado_display()} → {form.instance.get_estado_display()}")
        
        response = super().form_valid(form)
        
        if cambios:
            accion = 'SUSPENSION' if form.cleaned_data['estado'] == 'SUSPENDIDO' else \
                    'FINALIZACION' if form.cleaned_data['estado'] == 'FINALIZADO' else 'MODIFICACION'
            
            HistorialActividad.objects.create(
                actividad=self.object,
                accion=accion,
                usuario=self.request.user,
                descripcion=f"Actividad modificada: {'; '.join(cambios)}"
            )
            
            messages.success(self.request, 'Actividad actualizada correctamente')
        
        return response
    
    def get_success_url(self):
        return reverse_lazy('configuracion:actividad_detalle', kwargs={'pk': self.object.pk})


class StaffEditarView(LoginRequiredMixin, UpdateView):
    model = None
    template_name = 'configuracion/staff_editar_form.html'
    
    def get_object(self):
        from legajos.models import StaffActividad
        return get_object_or_404(StaffActividad, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff'] = self.get_object()
        return context
    
    def post(self, request, *args, **kwargs):
        from legajos.models import StaffActividad, HistorialStaff
        from django.contrib import messages
        
        staff = self.get_object()
        nuevo_rol = request.POST.get('rol_en_actividad')
        activo = request.POST.get('activo') == 'on'
        
        cambios = []
        if staff.rol_en_actividad != nuevo_rol:
            cambios.append(f"Rol: '{staff.rol_en_actividad}' → '{nuevo_rol}'")
            staff.rol_en_actividad = nuevo_rol
        
        if staff.activo != activo:
            cambios.append(f"Estado: {'Activo' if staff.activo else 'Inactivo'} → {'Activo' if activo else 'Inactivo'}")
            staff.activo = activo
        
        if cambios:
            staff.save()
            
            accion = 'DESASIGNACION' if not activo else 'CAMBIO_ROL'
            HistorialStaff.objects.create(
                staff=staff,
                accion=accion,
                usuario=request.user,
                descripcion=f'Staff modificado: {"; ".join(cambios)}'
            )
            
            messages.success(request, 'Staff actualizado correctamente')
        
        return redirect('configuracion:actividad_detalle', pk=staff.actividad.pk)


class StaffDesasignarView(LoginRequiredMixin, UpdateView):
    model = None
    
    def post(self, request, *args, **kwargs):
        from legajos.models import StaffActividad, HistorialStaff
        from django.contrib import messages
        
        staff = get_object_or_404(StaffActividad, pk=kwargs['pk'])
        staff.activo = False
        staff.save()
        
        HistorialStaff.objects.create(
            staff=staff,
            accion='DESASIGNACION',
            usuario=request.user,
            descripcion=f'{staff.personal.nombre} {staff.personal.apellido} desasignado de {staff.actividad.nombre}'
        )
        
        messages.success(request, f'{staff.personal.nombre_completo} desasignado de la actividad')
        return redirect('configuracion:actividad_detalle', pk=staff.actividad.pk)


class AsistenciaView(LoginRequiredMixin, DetailView):
    model = PlanFortalecimiento
    template_name = 'configuracion/asistencia.html'
    context_object_name = 'actividad'
    
    def get_context_data(self, **kwargs):
        from legajos.models import InscriptoActividad, RegistroAsistencia
        from datetime import datetime
        
        context = super().get_context_data(**kwargs)
        actividad = self.get_object()
        
        # Obtener fecha actual o la seleccionada
        fecha_str = self.request.GET.get('fecha')
        if fecha_str:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        else:
            fecha = datetime.now().date()
        
        context['fecha_actual'] = fecha
        
        # Obtener inscritos activos con su asistencia del día
        inscritos = InscriptoActividad.objects.filter(
            actividad=actividad,
            estado__in=['INSCRITO', 'ACTIVO']
        ).select_related('ciudadano', 'actividad').order_by('ciudadano__apellido')
        
        # Agregar asistencia actual a cada inscripto
        for inscripto in inscritos:
            try:
                inscripto.asistencia_actual = RegistroAsistencia.objects.get(
                    inscripto=inscripto,
                    fecha=fecha
                )
            except RegistroAsistencia.DoesNotExist:
                inscripto.asistencia_actual = None
        
        context['inscritos'] = inscritos
        
        return context


class RegistrarAsistenciaView(LoginRequiredMixin, UpdateView):
    model = None
    
    def post(self, request, *args, **kwargs):
        from legajos.models import InscriptoActividad, RegistroAsistencia, AlertaAusentismo
        from django.utils import timezone
        from django.contrib import messages
        from datetime import datetime, timedelta
        
        fecha_str = request.POST.get('fecha')
        actividad_id = request.POST.get('actividad_id')
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        actividad = get_object_or_404(PlanFortalecimiento, pk=actividad_id)
        
        # Procesar asistencias
        for key, value in request.POST.items():
            if key.startswith('asistencia_'):
                inscripto_id = key.replace('asistencia_', '')
                inscripto = get_object_or_404(InscriptoActividad, pk=inscripto_id)
                
                # Crear o actualizar registro
                registro, created = RegistroAsistencia.objects.get_or_create(
                    inscripto=inscripto,
                    fecha=fecha,
                    defaults={
                        'estado': value,
                        'registrado_por': request.user
                    }
                )
                
                if not created:
                    registro.estado = value
                    registro.registrado_por = request.user
                    registro.save()
                
                # Verificar ausentismo si está ausente
                if value == 'AUSENTE':
                    self._verificar_ausentismo(inscripto, fecha)
        
        messages.success(request, f'Asistencia registrada para {fecha.strftime("%d/%m/%Y")}')
        return redirect('configuracion:asistencia', pk=actividad_id)
    
    def _verificar_ausentismo(self, inscripto, fecha):
        from legajos.models import RegistroAsistencia, AlertaAusentismo
        from datetime import timedelta
        
        # Contar días consecutivos de ausencia
        dias_ausente = 0
        fecha_actual = fecha
        
        while True:
            try:
                registro = RegistroAsistencia.objects.get(
                    inscripto=inscripto,
                    fecha=fecha_actual
                )
                if registro.estado == 'AUSENTE':
                    dias_ausente += 1
                    fecha_actual -= timedelta(days=1)
                else:
                    break
            except RegistroAsistencia.DoesNotExist:
                break
        
        # Crear alerta si es necesario
        if dias_ausente >= 3:
            tipo_alerta = 'AUSENTISMO_5' if dias_ausente >= 5 else 'AUSENTISMO_3'
            
            AlertaAusentismo.objects.get_or_create(
                inscripto=inscripto,
                tipo=tipo_alerta,
                defaults={
                    'dias_ausente': dias_ausente,
                    'fecha_inicio_ausencia': fecha_actual + timedelta(days=1)
                }
            )