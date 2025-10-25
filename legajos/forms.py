from django import forms
from .models import Ciudadano, LegajoAtencion, Consentimiento, EvaluacionInicial
from core.models import DispositivoRed
import json


class ConsultaRenaperForm(forms.Form):
    """Formulario para consultar datos en RENAPER"""
    
    GENERO_CHOICES = [
        ('', 'Seleccionar...'),
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('X', 'No binario'),
    ]
    
    dni = forms.CharField(
        max_length=8,
        label='DNI',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': 'Ingrese el DNI (ej: 12345678)'
        })
    )
    
    sexo = forms.ChoiceField(
        choices=GENERO_CHOICES,
        label='Sexo',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
    )
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            # Limpiar el DNI de caracteres no numéricos
            dni_limpio = ''.join(filter(str.isdigit, dni))
            
            # Validar que tenga 7 u 8 dígitos
            if len(dni_limpio) < 7 or len(dni_limpio) > 8:
                raise forms.ValidationError('El DNI debe tener entre 7 y 8 dígitos.')
            
            return dni_limpio
        
        return dni


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


class EvaluacionInicialForm(forms.ModelForm):
    """Formulario para evaluación inicial"""
    
    # Campos adicionales para tamizajes comunes
    assist_puntaje = forms.IntegerField(
        required=False,
        label='ASSIST - Puntaje Total',
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'min': '0',
            'max': '100'
        })
    )
    
    phq9_puntaje = forms.IntegerField(
        required=False,
        label='PHQ-9 - Puntaje Total',
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'min': '0',
            'max': '27'
        })
    )
    
    class Meta:
        model = EvaluacionInicial
        fields = [
            'situacion_consumo', 'antecedentes', 'red_apoyo', 'condicion_social',
            'riesgo_suicida', 'violencia'
        ]
        widgets = {
            'situacion_consumo': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Describe la situación actual de consumo...'
            }),
            'antecedentes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Antecedentes médicos, psiquiátricos y de consumo...'
            }),
            'red_apoyo': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Describe la red de apoyo familiar y social...'
            }),
            'condicion_social': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Situación socioeconómica, vivienda, trabajo, educación...'
            }),
            'riesgo_suicida': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-red-600 shadow-sm focus:border-red-500 focus:ring-red-500'
            }),
            'violencia': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-red-600 shadow-sm focus:border-red-500 focus:ring-red-500'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar datos de tamizajes si existen
        if self.instance and self.instance.tamizajes:
            tamizajes = self.instance.tamizajes
            if 'ASSIST' in tamizajes:
                self.fields['assist_puntaje'].initial = tamizajes['ASSIST'].get('puntaje')
            if 'PHQ9' in tamizajes:
                self.fields['phq9_puntaje'].initial = tamizajes['PHQ9'].get('puntaje')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Construir JSON de tamizajes
        tamizajes = {}
        
        assist_puntaje = self.cleaned_data.get('assist_puntaje')
        if assist_puntaje is not None:
            tamizajes['ASSIST'] = {
                'puntaje': assist_puntaje,
                'fecha': self.cleaned_data.get('fecha_assist') or str(instance.modificado.date() if instance.pk else instance.creado.date())
            }
        
        phq9_puntaje = self.cleaned_data.get('phq9_puntaje')
        if phq9_puntaje is not None:
            tamizajes['PHQ9'] = {
                'puntaje': phq9_puntaje,
                'fecha': self.cleaned_data.get('fecha_phq9') or str(instance.modificado.date() if instance.pk else instance.creado.date())
            }
        
        instance.tamizajes = tamizajes if tamizajes else None
        
        if commit:
            instance.save()
        return instance