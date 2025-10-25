from django import forms
from .models import Ciudadano, LegajoAtencion, Consentimiento
from core.models import DispositivoRed


class ConsultaRenaperForm(forms.Form):
    """Formulario para consultar datos en RENAPER"""
    
    GENERO_CHOICES = [
        ('', 'Seleccionar...'),
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('X', 'No binario'),
    ]
    
    cuit = forms.CharField(
        max_length=13,
        label='CUIT',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': 'Ingrese el CUIT (ej: 20-12345678-9)'
        })
    )
    
    sexo = forms.ChoiceField(
        choices=GENERO_CHOICES,
        label='Sexo',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
    )


class CiudadanoForm(forms.ModelForm):
    """Formulario para crear/editar ciudadanos con datos de RENAPER"""
    
    class Meta:
        model = Ciudadano
        fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'telefono', 'email', 'domicilio']
        widgets = {
            'dni': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'readonly': True
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'type': 'date'
            }),
            'genero': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'domicilio': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
        }


class BuscarCiudadanoForm(forms.Form):
    """Paso 1: Buscar ciudadano para el legajo"""
    
    dni = forms.CharField(
        max_length=20,
        label='DNI del Ciudadano',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': 'Ingrese el DNI'
        })
    )


class AdmisionLegajoForm(forms.ModelForm):
    """Paso 2: Datos de admisión del legajo"""
    
    class Meta:
        model = LegajoAtencion
        fields = ['dispositivo', 'via_ingreso', 'nivel_riesgo', 'notas']
        widgets = {
            'dispositivo': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'via_ingreso': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'nivel_riesgo': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Observaciones iniciales (opcional)'
            }),
        }


class ConsentimientoForm(forms.ModelForm):
    """Formulario para consentimientos"""
    
    class Meta:
        model = Consentimiento
        fields = ['texto', 'firmado_por', 'fecha_firma', 'archivo']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 6,
                'placeholder': 'Texto del consentimiento informado'
            }),
            'firmado_por': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Nombre completo de quien firma'
            }),
            'fecha_firma': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'type': 'date'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }