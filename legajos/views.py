from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from .models import Ciudadano, LegajoAtencion, EvaluacionInicial
from core.models import DispositivoRed
from .forms import ConsultaRenaperForm, CiudadanoForm, BuscarCiudadanoForm, AdmisionLegajoForm, ConsentimientoForm, EvaluacionInicialForm
from .services.consulta_renaper import consultar_datos_renaper


class CiudadanoListView(LoginRequiredMixin, ListView):
    model = Ciudadano
    template_name = 'legajos/ciudadano_list.html'
    context_object_name = 'ciudadanos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Ciudadano.objects.filter(activo=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(dni__icontains=search) |
                Q(nombre__icontains=search) |
                Q(apellido__icontains=search)
            )
        return queryset.order_by('apellido', 'nombre')


class CiudadanoDetailView(LoginRequiredMixin, DetailView):
    model = Ciudadano
    template_name = 'legajos/ciudadano_detail.html'
    context_object_name = 'ciudadano'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legajos'] = self.object.legajos.all().order_by('-fecha_apertura')
        return context


class CiudadanoCreateView(LoginRequiredMixin, FormView):
    """Vista para crear ciudadanos con integración RENAPER"""
    template_name = 'legajos/ciudadano_renaper_form.html'
    form_class = ConsultaRenaperForm
    
    def extraer_dni_de_cuit(self, cuit):
        """Extrae el DNI del CUIT (formato XX-XXXXXXXX-X)"""
        import re
        # Limpiar el CUIT de guiones y espacios
        cuit_limpio = re.sub(r'[^0-9]', '', cuit)
        
        # Verificar que tenga 11 dígitos
        if len(cuit_limpio) != 11:
            return None
            
        # Extraer DNI (dígitos 3 al 10)
        dni = cuit_limpio[2:10]
        
        # Verificar que el DNI tenga 8 dígitos
        if len(dni) != 8:
            return None
            
        return dni
    
    def form_valid(self, form):
        dni = form.cleaned_data['dni']
        sexo = form.cleaned_data['sexo']
        
        # Verificar si el ciudadano ya existe
        if Ciudadano.objects.filter(dni=dni).exists():
            messages.error(self.request, f'Ya existe un ciudadano con DNI {dni}')
            return self.form_invalid(form)
        
        # Consultar RENAPER
        resultado = consultar_datos_renaper(dni, sexo)
        
        if not resultado['success']:
            # Guardar datos para mostrar opción manual
            context = self.get_context_data(form=form)
            context['renaper_error'] = True
            context['dni_consultado'] = dni
            context['sexo_consultado'] = sexo
            
            if resultado.get('fallecido'):
                context['error_message'] = 'La persona consultada figura como fallecida en RENAPER'
            else:
                context['error_message'] = f'No se encontraron datos en RENAPER: {resultado.get("error", "Error desconocido")}'
            
            return self.render_to_response(context)
        
        # Guardar datos en sesión para el siguiente paso
        self.request.session['datos_renaper'] = resultado['data']
        self.request.session['datos_api_renaper'] = resultado.get('datos_api', {})
        
        return redirect('legajos:ciudadano_confirmar')


class CiudadanoManualView(LoginRequiredMixin, CreateView):
    """Vista para crear ciudadanos manualmente cuando RENAPER falla"""
    model = Ciudadano
    form_class = CiudadanoForm
    template_name = 'legajos/ciudadano_manual_form.html'
    success_url = reverse_lazy('legajos:ciudadanos')
    
    def get_initial(self):
        """Prellenar DNI y sexo si vienen de RENAPER"""
        initial = super().get_initial()
        cuit = self.request.GET.get('cuit')
        sexo = self.request.GET.get('sexo')
        
        if cuit:
            # Extraer DNI del CUIT
            import re
            cuit_limpio = re.sub(r'[^0-9]', '', cuit)
            if len(cuit_limpio) == 11:
                dni = cuit_limpio[2:10]
                initial['dni'] = dni
        if sexo:
            initial['genero'] = sexo
            
        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Ciudadano {self.object.nombre} {self.object.apellido} creado exitosamente (carga manual)')
        return response


class CiudadanoConfirmarView(LoginRequiredMixin, CreateView):
    """Vista para confirmar y completar datos del ciudadano"""
    model = Ciudadano
    form_class = CiudadanoForm
    template_name = 'legajos/ciudadano_confirmar_form.html'
    success_url = reverse_lazy('legajos:ciudadanos')
    
    def dispatch(self, request, *args, **kwargs):
        if 'datos_renaper' not in request.session:
            messages.error(request, 'No hay datos de RENAPER disponibles. Inicie el proceso nuevamente.')
            return redirect('legajos:ciudadano_nuevo')
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        """Prellenar el formulario con datos de RENAPER"""
        datos = self.request.session.get('datos_renaper', {})
        return {
            'dni': datos.get('dni'),
            'nombre': datos.get('nombre'),
            'apellido': datos.get('apellido'),
            'fecha_nacimiento': datos.get('fecha_nacimiento'),
            'genero': datos.get('genero'),
            'domicilio': datos.get('domicilio'),
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datos_api'] = self.request.session.get('datos_api_renaper', {})
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Limpiar datos de sesión
        self.request.session.pop('datos_renaper', None)
        self.request.session.pop('datos_api_renaper', None)
        messages.success(self.request, f'Ciudadano {self.object.nombre} {self.object.apellido} creado exitosamente')
        return response


class CiudadanoUpdateView(LoginRequiredMixin, UpdateView):
    model = Ciudadano
    form_class = CiudadanoForm
    template_name = 'legajos/ciudadano_edit_form.html'
    
    def get_success_url(self):
        return reverse_lazy('legajos:ciudadano_detalle', kwargs={'pk': self.object.pk})


class LegajoListView(LoginRequiredMixin, ListView):
    model = LegajoAtencion
    template_name = 'legajos/legajo_list.html'
    context_object_name = 'legajos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = LegajoAtencion.objects.select_related('ciudadano', 'dispositivo')
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset.order_by('-fecha_apertura')


class LegajoDetailView(LoginRequiredMixin, DetailView):
    model = LegajoAtencion
    template_name = 'legajos/legajo_detail.html'
    context_object_name = 'legajo'


class AdmisionPaso1View(LoginRequiredMixin, FormView):
    """Paso 1: Buscar ciudadano"""
    template_name = 'legajos/admision_paso1.html'
    form_class = BuscarCiudadanoForm
    
    def get(self, request, *args, **kwargs):
        # Si viene con ciudadano preseleccionado, ir directo al paso 2
        ciudadano_id = request.GET.get('ciudadano')
        if ciudadano_id:
            try:
                ciudadano = Ciudadano.objects.get(id=ciudadano_id, activo=True)
                request.session['admision_ciudadano_id'] = ciudadano.id
                return redirect('legajos:admision_paso2')
            except Ciudadano.DoesNotExist:
                messages.error(request, 'Ciudadano no encontrado')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        dni = form.cleaned_data['dni']
        
        try:
            ciudadano = Ciudadano.objects.get(dni=dni, activo=True)
            self.request.session['admision_ciudadano_id'] = ciudadano.id
            return redirect('legajos:admision_paso2')
        except Ciudadano.DoesNotExist:
            messages.error(self.request, f'No se encontró un ciudadano con DNI {dni}. Debe crear el ciudadano primero.')
            return self.form_invalid(form)


class AdmisionPaso2View(LoginRequiredMixin, CreateView):
    """Paso 2: Datos de admisión"""
    model = LegajoAtencion
    form_class = AdmisionLegajoForm
    template_name = 'legajos/admision_paso2.html'
    
    def dispatch(self, request, *args, **kwargs):
        if 'admision_ciudadano_id' not in request.session:
            messages.error(request, 'Debe seleccionar un ciudadano primero.')
            return redirect('legajos:admision_paso1')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ciudadano_id = self.request.session.get('admision_ciudadano_id')
        context['ciudadano'] = get_object_or_404(Ciudadano, id=ciudadano_id)
        context['dispositivos'] = DispositivoRed.objects.filter(activo=True).order_by('nombre')
        return context
    
    def form_valid(self, form):
        ciudadano_id = self.request.session.get('admision_ciudadano_id')
        form.instance.ciudadano_id = ciudadano_id
        form.instance.responsable = self.request.user
        
        response = super().form_valid(form)
        
        # Limpiar sesión y guardar ID del legajo para paso 3
        self.request.session.pop('admision_ciudadano_id', None)
        self.request.session['admision_legajo_id'] = self.object.id
        
        return redirect('legajos:admision_paso3')


class AdmisionPaso3View(LoginRequiredMixin, FormView):
    """Paso 3: Consentimiento (opcional)"""
    template_name = 'legajos/admision_paso3.html'
    form_class = ConsentimientoForm
    
    def dispatch(self, request, *args, **kwargs):
        if 'admision_legajo_id' not in request.session:
            messages.error(request, 'Proceso de admisión inválido.')
            return redirect('legajos:admision_paso1')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        legajo_id = self.request.session.get('admision_legajo_id')
        context['legajo'] = get_object_or_404(LegajoAtencion, id=legajo_id)
        return context
    
    def form_valid(self, form):
        legajo_id = self.request.session.get('admision_legajo_id')
        legajo = get_object_or_404(LegajoAtencion, id=legajo_id)
        
        form.instance.ciudadano = legajo.ciudadano
        form.save()
        
        # Limpiar sesión
        self.request.session.pop('admision_legajo_id', None)
        
        messages.success(self.request, f'Legajo {legajo.codigo} creado exitosamente con consentimiento.')
        return redirect('legajos:detalle', pk=legajo.id)
    
    def get(self, request, *args, **kwargs):
        # Permitir saltar este paso
        if request.GET.get('skip') == '1':
            legajo_id = request.session.get('admision_legajo_id')
            legajo = get_object_or_404(LegajoAtencion, id=legajo_id)
            request.session.pop('admision_legajo_id', None)
            messages.success(request, f'Legajo {legajo.codigo} creado exitosamente.')
            return redirect('legajos:detalle', pk=legajo.id)
        
        return super().get(request, *args, **kwargs)


class EvaluacionInicialView(LoginRequiredMixin, UpdateView):
    """Vista para crear/editar evaluación inicial"""
    model = EvaluacionInicial
    form_class = EvaluacionInicialForm
    template_name = 'legajos/evaluacion_form.html'
    
    def get_object(self, queryset=None):
        legajo_id = self.kwargs.get('legajo_id')
        legajo = get_object_or_404(LegajoAtencion, id=legajo_id)
        
        # Crear evaluación si no existe (OneToOne)
        evaluacion, created = EvaluacionInicial.objects.get_or_create(
            legajo=legajo,
            defaults={}
        )
        return evaluacion
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legajo'] = self.object.legajo
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Evaluación inicial guardada exitosamente.')
        return reverse_lazy('legajos:detalle', kwargs={'pk': self.object.legajo.id})