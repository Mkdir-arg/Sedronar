from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CustomUserChangeForm, UserCreationForm
from .services import UsuariosService


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Administrador').exists()


class UsuariosLoginView(LoginView):
    template_name = "user/login.html"


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "user/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return UsuariosService.get_filtered_usuarios(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Configuración para el componente data_table
        context.update(UsuariosService.get_usuarios_list_context())
        return context


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "user/user_form.html"
    success_url = reverse_lazy("usuarios")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_groups'] = Group.objects.all().order_by('name')
        return context
    
    def form_valid(self, form):
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            response = super().form_valid(form)
            
            # Verificar que el usuario se guardó correctamente
            user = self.object
            groups = form.cleaned_data.get('groups', [])
            
            logger.info(f"Usuario creado: {user.username}")
            logger.info(f"Grupos asignados: {[g.name for g in groups]}")
            logger.info(f"Grupos en BD: {[g.name for g in user.groups.all()]}")
            
            # Verificar que los grupos se asignaron
            if groups and user.groups.count() == 0:
                logger.error(f"Error: Los grupos no se asignaron al usuario {user.username}")
                # Intentar reasignar
                user.groups.set(groups)
                logger.info(f"Grupos reasignados: {[g.name for g in user.groups.all()]}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error al crear usuario: {str(e)}")
            form.add_error(None, f"Error al guardar el usuario: {str(e)}")
            return self.form_invalid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "user/user_form.html"
    success_url = reverse_lazy("usuarios")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_groups'] = Group.objects.all().order_by('name')
        return context
    
    def form_valid(self, form):
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            response = super().form_valid(form)
            
            # Verificar que el usuario se actualizó correctamente
            user = self.object
            groups = form.cleaned_data.get('groups', [])
            
            logger.info(f"Usuario actualizado: {user.username}")
            logger.info(f"Grupos asignados: {[g.name for g in groups]}")
            logger.info(f"Grupos en BD: {[g.name for g in user.groups.all()]}")
            
            # Verificar que los grupos se asignaron
            if groups and user.groups.count() == 0:
                logger.error(f"Error: Los grupos no se asignaron al usuario {user.username}")
                # Intentar reasignar
                user.groups.set(groups)
                logger.info(f"Grupos reasignados: {[g.name for g in user.groups.all()]}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error al actualizar usuario: {str(e)}")
            form.add_error(None, f"Error al actualizar el usuario: {str(e)}")
            return self.form_invalid(form)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = "user/user_confirm_delete.html"
    success_url = reverse_lazy("usuarios")


class GroupListView(AdminRequiredMixin, ListView):
    model = Group
    template_name = "group/group_list.html"
    context_object_name = "groups"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Configuración para el componente data_table
        context["table_headers"] = [
            {"title": "Nombre"},
        ]

        context["table_fields"] = [
            {"name": "name"},
        ]

        return context
