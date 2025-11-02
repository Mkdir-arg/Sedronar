from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from core.models import Provincia, Municipio, Localidad, Institucion
from legajos.models import LegajoInstitucional, PersonalInstitucion, EvaluacionInstitucional, PlanFortalecimiento, IndicadorInstitucional, StaffActividad
from .forms import ProvinciaForm, MunicipioForm, LocalidadForm, InstitucionForm

# Alias para compatibilidad
DispositivoRed = Institucion
DispositivoForm = InstitucionForm


class ProvinciaListView(LoginRequiredMixin, ListView):
    model = Provincia
    template_name = 'configuracion/provincia_list.html'
    context_object_name = 'provincias'
    paginate_by = 20


class ProvinciaCreateView(LoginRequiredMixin, CreateView):
    model = Provincia
    form_class = ProvinciaForm
    template_name = 'configuracion/provincia_form.html'
    success_url = reverse_lazy('configuracion:provincias')


class ProvinciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Provincia
    form_class = ProvinciaForm
    template_name = 'configuracion/provincia_form.html'
    success_url = reverse_lazy('configuracion:provincias')


class ProvinciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Provincia
    template_name = 'configuracion/provincia_confirm_delete.html'
    success_url = reverse_lazy('configuracion:provincias')


class MunicipioListView(LoginRequiredMixin, ListView):
    model = Municipio
    template_name = 'configuracion/municipio_list.html'
    context_object_name = 'municipios'
    paginate_by = 20


class MunicipioCreateView(LoginRequiredMixin, CreateView):
    model = Municipio
    form_class = MunicipioForm
    template_name = 'configuracion/municipio_form.html'
    success_url = reverse_lazy('configuracion:municipios')


class MunicipioUpdateView(LoginRequiredMixin, UpdateView):
    model = Municipio
    form_class = MunicipioForm
    template_name = 'configuracion/municipio_form.html'
    success_url = reverse_lazy('configuracion:municipios')


class MunicipioDeleteView(LoginRequiredMixin, DeleteView):
    model = Municipio
    template_name = 'configuracion/municipio_confirm_delete.html'
    success_url = reverse_lazy('configuracion:municipios')


class LocalidadListView(LoginRequiredMixin, ListView):
    model = Localidad
    template_name = 'configuracion/localidad_list.html'
    context_object_name = 'localidades'
    paginate_by = 20


class LocalidadCreateView(LoginRequiredMixin, CreateView):
    model = Localidad
    form_class = LocalidadForm
    template_name = 'configuracion/localidad_form.html'
    success_url = reverse_lazy('configuracion:localidades')


class LocalidadUpdateView(LoginRequiredMixin, UpdateView):
    model = Localidad
    form_class = LocalidadForm
    template_name = 'configuracion/localidad_form.html'
    success_url = reverse_lazy('configuracion:localidades')


class LocalidadDeleteView(LoginRequiredMixin, DeleteView):
    model = Localidad
    template_name = 'configuracion/localidad_confirm_delete.html'
    success_url = reverse_lazy('configuracion:localidades')


class InstitucionListView(LoginRequiredMixin, ListView):
    model = Institucion
    template_name = 'configuracion/institucion_list.html'
    context_object_name = 'instituciones'
    paginate_by = 20
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            # Super admin ve todas las instituciones aprobadas
            return Institucion.objects.filter(
                estado_registro='APROBADO'
            ).order_by('nombre')
        else:
            # Usuario normal ve solo instituciones aprobadas donde es encargado
            return Institucion.objects.filter(
                encargados=self.request.user,
                estado_registro='APROBADO'
            ).order_by('nombre')


# Alias para compatibilidad
DispositivoListView = InstitucionListView


class InstitucionCreateView(LoginRequiredMixin, CreateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'configuracion/institucion_form.html'
    success_url = reverse_lazy('configuracion:instituciones')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            from django.contrib import messages
            messages.error(request, 'No tiene permisos para crear instituciones.')
            return redirect('configuracion:instituciones')
        return super().dispatch(request, *args, **kwargs)


# Alias para compatibilidad
DispositivoCreateView = InstitucionCreateView


class InstitucionUpdateView(LoginRequiredMixin, UpdateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'configuracion/institucion_form.html'
    success_url = reverse_lazy('configuracion:instituciones')
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Institucion.objects.all()
        else:
            return Institucion.objects.filter(encargados=self.request.user)


# Alias para compatibilidad
DispositivoUpdateView = InstitucionUpdateView


class InstitucionDeleteView(LoginRequiredMixin, DeleteView):
    model = Institucion
    template_name = 'configuracion/institucion_confirm_delete.html'
    success_url = reverse_lazy('configuracion:instituciones')
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Institucion.objects.all()
        else:
            return Institucion.objects.filter(encargados=self.request.user)


class InstitucionDetailView(LoginRequiredMixin, DetailView):
    model = Institucion
    template_name = 'configuracion/institucion_detail.html'
    context_object_name = 'institucion'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        institucion = self.get_object()
        
        # Obtener o crear legajo institucional
        legajo, created = LegajoInstitucional.objects.get_or_create(
            institucion=institucion,
            defaults={'estado': 'ACTIVO'}
        )
        
        context['legajo'] = legajo
        context['personal'] = PersonalInstitucion.objects.filter(legajo_institucional=legajo)
        context['evaluaciones'] = EvaluacionInstitucional.objects.filter(legajo_institucional=legajo).order_by('-fecha_evaluacion')
        context['planes'] = PlanFortalecimiento.objects.filter(legajo_institucional=legajo).order_by('-fecha_inicio')
        context['indicadores'] = IndicadorInstitucional.objects.filter(legajo_institucional=legajo).order_by('-periodo')
        
        return context




class PersonalInstitucionCreateView(LoginRequiredMixin, CreateView):
    model = PersonalInstitucion
    fields = ['nombre', 'apellido', 'dni', 'tipo', 'titulo_profesional', 'matricula', 'activo']
    template_name = 'configuracion/personal_form.html'
    
    def form_valid(self, form):
        institucion = get_object_or_404(Institucion, pk=self.kwargs['institucion_pk'])
        legajo, created = LegajoInstitucional.objects.get_or_create(
            institucion=institucion,
            defaults={'estado': 'ACTIVO'}
        )
        form.instance.legajo_institucional = legajo
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('configuracion:institucion_detalle', kwargs={'pk': self.kwargs['institucion_pk']})


class EvaluacionInstitucionCreateView(LoginRequiredMixin, CreateView):
    model = EvaluacionInstitucional
    fields = ['fecha_evaluacion', 'observaciones']
    template_name = 'configuracion/evaluacion_form.html'
    
    def form_valid(self, form):
        institucion = get_object_or_404(Institucion, pk=self.kwargs['institucion_pk'])
        legajo, created = LegajoInstitucional.objects.get_or_create(
            institucion=institucion,
            defaults={'estado': 'ACTIVO'}
        )
        form.instance.legajo_institucional = legajo
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('configuracion:institucion_detalle', kwargs={'pk': self.kwargs['institucion_pk']})


class PlanFortalecimientoCreateView(LoginRequiredMixin, CreateView):
    model = PlanFortalecimiento
    fields = ['nombre', 'tipo', 'subtipo', 'descripcion', 'cupo_ciudadanos', 'fecha_inicio', 'fecha_fin', 'estado']
    template_name = 'configuracion/plan_form.html'
    
    def form_valid(self, form):
        institucion = get_object_or_404(Institucion, pk=self.kwargs['institucion_pk'])
        legajo, created = LegajoInstitucional.objects.get_or_create(
            institucion=institucion,
            defaults={'estado': 'ACTIVO'}
        )
        form.instance.legajo_institucional = legajo
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('configuracion:institucion_detalle', kwargs={'pk': self.kwargs['institucion_pk']})


class IndicadorInstitucionCreateView(LoginRequiredMixin, CreateView):
    model = IndicadorInstitucional
    fields = ['periodo', 'observaciones']
    template_name = 'configuracion/indicador_form.html'
    
    def form_valid(self, form):
        institucion = get_object_or_404(Institucion, pk=self.kwargs['institucion_pk'])
        legajo, created = LegajoInstitucional.objects.get_or_create(
            institucion=institucion,
            defaults={'estado': 'ACTIVO'}
        )
        form.instance.legajo_institucional = legajo
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('configuracion:institucion_detalle', kwargs={'pk': self.kwargs['institucion_pk']})