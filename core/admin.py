from django.contrib import admin

from core.models import (
    Localidad,
    Provincia,
    Municipio,
    Sexo,
    Mes,
    Dia,
    Turno,
    DispositivoRed,
)

admin.site.register(Provincia)
admin.site.register(Municipio)
admin.site.register(Sexo)
admin.site.register(Mes)
admin.site.register(Dia)
admin.site.register(Turno)


@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "municipio":
            provincia_id = request.GET.get("provincia")
            if provincia_id:
                kwargs["queryset"] = Municipio.objects.filter(provincia_id=provincia_id)
            else:
                kwargs["queryset"] = Municipio.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(DispositivoRed)
class DispositivoRedAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "activo", "municipio", "provincia")
    list_filter = ("tipo", "activo", "provincia")
    search_fields = ("nombre", "municipio__nombre", "provincia__nombre")
    ordering = ("provincia", "municipio", "nombre")
    
    fieldsets = (
        ("Información Básica", {
            "fields": ("nombre", "tipo", "activo")
        }),
        ("Ubicación", {
            "fields": ("provincia", "municipio", "localidad", "direccion")
        }),
        ("Contacto", {
            "fields": ("telefono", "email")
        }),
        ("Registro", {
            "fields": ("nro_registro", "resolucion", "fecha_alta")
        }),
        ("Descripción", {
            "fields": ("descripcion",)
        }),
    )
