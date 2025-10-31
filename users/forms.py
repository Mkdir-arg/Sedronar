from django import forms
from django.contrib.auth.models import User, Group

from core.models import Provincia
from .models import Profile


def _normalize_groups_data(data):
    """
    Permite aceptar tanto 'groups' como 'groups[]' cuando el formulario se envía desde JS.
    Algunos frontends serializan listas como 'field[]', lo que hacía que Django ignorara el campo.
    """
    if not data:
        return data

    try:
        has_groups_key = "groups" in data
    except TypeError:
        # Si data no es iterable (raro en formularios), lo dejamos igual
        return data

    if has_groups_key or "groups[]" not in data:
        return data

    if hasattr(data, "getlist") and hasattr(data, "setlist"):
        mutable_data = data.copy()
        mutable_data.setlist("groups", mutable_data.getlist("groups[]"))
        try:
            del mutable_data["groups[]"]
        except KeyError:
            pass
        return mutable_data

    mutable_data = data.copy()
    raw_value = mutable_data.pop("groups[]", [])
    if isinstance(raw_value, (list, tuple)):
        values = list(raw_value)
    else:
        values = [raw_value]
    mutable_data["groups"] = values
    return mutable_data


def _normalize_groups_args(args, kwargs):
    if args:
        first = _normalize_groups_data(args[0])
        if first is not args[0]:
            args = (first, *args[1:])
    elif kwargs.get("data") is not None:
        kwargs["data"] = _normalize_groups_data(kwargs["data"])
    return args, kwargs


class UserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        args, kwargs = _normalize_groups_args(args, kwargs)
        super().__init__(*args, **kwargs)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Ingrese la contraseña'
        }), 
        label="Contraseña"
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'id': 'id_groups',
            'size': '4'
        }),
        label="Grupos",
    )
    es_usuario_provincial = forms.BooleanField(
        required=False,
        label="Es usuario provincial",
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
        })
    )
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        }),
        label="Provincia",
    )

    rol = forms.CharField(
        max_length=100, 
        required=False, 
        label="Rol",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Ingrese el rol'
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "groups",
            "es_usuario_provincial",
            "provincia",
            "last_name",
            "first_name",
            "rol",
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el apellido'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("es_usuario_provincial") and not cleaned.get("provincia"):
            self.add_error("provincia", "Seleccione una provincia.")
        return cleaned

    def save(self, commit=True):
        from django.db import transaction
        import logging
        
        logger = logging.getLogger(__name__)
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            with transaction.atomic():
                user.save()
                
                # Asegurar que los grupos se asignen correctamente
                groups = self.cleaned_data.get("groups", [])
                logger.info(f"Grupos a asignar: {[g.name for g in groups]}")
                
                # Usar set() en lugar de clear() + add() para mayor confiabilidad
                user.groups.set(groups)
                
                # Verificar que se asignaron correctamente
                assigned_groups = user.groups.all()
                logger.info(f"Grupos asignados en BD: {[g.name for g in assigned_groups]}")

                # Crear o actualizar perfil
                profile, created = Profile.objects.get_or_create(user=user)
                profile.es_usuario_provincial = self.cleaned_data.get(
                    "es_usuario_provincial", False
                )
                profile.provincia = (
                    self.cleaned_data.get("provincia")
                    if self.cleaned_data.get("es_usuario_provincial")
                    else None
                )
                profile.rol = self.cleaned_data.get("rol")
                profile.save()

        return user


class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Dejar en blanco para no cambiar'
        }),
        label="Contraseña (dejar en blanco para no cambiarla)",
        required=False,
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'id': 'id_groups_edit',
            'size': '4'
        }),
        label="Grupos",
    )
    es_usuario_provincial = forms.BooleanField(
        required=False,
        label="Es usuario provincial",
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
        })
    )
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        }),
        label="Provincia",
    )
    rol = forms.CharField(
        max_length=100, 
        required=False, 
        label="Rol",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Ingrese el rol'
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "groups",
            "es_usuario_provincial",
            "provincia",
            "last_name",
            "first_name",
            "rol",
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ingrese el apellido'
            }),
        }

    def __init__(self, *args, **kwargs):
        args, kwargs = _normalize_groups_args(args, kwargs)
        super().__init__(*args, **kwargs)
        self._original_password_hash = self.instance.password
        self.fields["password"].initial = ""

        # Inicializar con datos del profile si existe
        try:
            prof = self.instance.profile
        except Profile.DoesNotExist:
            prof = None

        if prof:
            self.fields["es_usuario_provincial"].initial = prof.es_usuario_provincial
            self.fields["provincia"].initial = prof.provincia
            self.fields["rol"].initial = prof.rol

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("es_usuario_provincial") and not cleaned.get("provincia"):
            self.add_error("provincia", "Seleccione una provincia.")
        return cleaned

    def save(self, commit=True):
        from django.db import transaction
        import logging
        
        logger = logging.getLogger(__name__)
        new_pwd = self.cleaned_data.get("password")
        user = super().save(commit=False)

        if new_pwd:
            user.set_password(new_pwd)
        else:
            user.password = self._original_password_hash

        if commit:
            with transaction.atomic():
                user.save()
                
                # Asegurar que los grupos se asignen correctamente
                groups = self.cleaned_data.get("groups", [])
                logger.info(f"Grupos a asignar: {[g.name for g in groups]}")
                
                # Usar set() en lugar de clear() + add() para mayor confiabilidad
                user.groups.set(groups)
                
                # Verificar que se asignaron correctamente
                assigned_groups = user.groups.all()
                logger.info(f"Grupos asignados en BD: {[g.name for g in assigned_groups]}")

                # Crear o actualizar perfil
                profile, created = Profile.objects.get_or_create(user=user)
                profile.es_usuario_provincial = self.cleaned_data.get(
                    "es_usuario_provincial", False
                )
                profile.provincia = (
                    self.cleaned_data.get("provincia")
                    if self.cleaned_data.get("es_usuario_provincial")
                    else None
                )
                profile.rol = self.cleaned_data.get("rol")
                profile.save()

        return user
