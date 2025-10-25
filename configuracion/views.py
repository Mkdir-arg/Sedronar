from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Provincia, Municipio, Localidad, DispositivoRed
from .forms import ProvinciaForm, MunicipioForm, LocalidadForm, DispositivoForm


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


class DispositivoListView(LoginRequiredMixin, ListView):
    model = DispositivoRed
    template_name = 'configuracion/dispositivo_list.html'
    context_object_name = 'dispositivos'
    paginate_by = 20


class DispositivoCreateView(LoginRequiredMixin, CreateView):
    model = DispositivoRed
    form_class = DispositivoForm
    template_name = 'configuracion/dispositivo_form.html'
    success_url = reverse_lazy('configuracion:dispositivos')


class DispositivoUpdateView(LoginRequiredMixin, UpdateView):
    model = DispositivoRed
    form_class = DispositivoForm
    template_name = 'configuracion/dispositivo_form.html'
    success_url = reverse_lazy('configuracion:dispositivos')


class DispositivoDeleteView(LoginRequiredMixin, DeleteView):
    model = DispositivoRed
    template_name = 'configuracion/dispositivo_confirm_delete.html'
    success_url = reverse_lazy('configuracion:dispositivos')