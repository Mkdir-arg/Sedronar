from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Ciudadano, LegajoAtencion
from core.models import DispositivoRed


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


class CiudadanoCreateView(LoginRequiredMixin, CreateView):
    model = Ciudadano
    template_name = 'legajos/ciudadano_form.html'
    fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'telefono', 'email', 'domicilio']
    success_url = reverse_lazy('legajos:ciudadanos')


class CiudadanoUpdateView(LoginRequiredMixin, UpdateView):
    model = Ciudadano
    template_name = 'legajos/ciudadano_form.html'
    fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'telefono', 'email', 'domicilio']
    
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


class LegajoCreateView(LoginRequiredMixin, CreateView):
    model = LegajoAtencion
    template_name = 'legajos/legajo_form.html'
    fields = ['ciudadano', 'dispositivo', 'via_ingreso', 'nivel_riesgo', 'confidencialidad', 'notas']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ciudadanos'] = Ciudadano.objects.filter(activo=True).order_by('apellido', 'nombre')
        context['dispositivos'] = DispositivoRed.objects.filter(activo=True).order_by('nombre')
        return context
    
    def form_valid(self, form):
        form.instance.responsable = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('legajos:detalle', kwargs={'pk': self.object.pk})