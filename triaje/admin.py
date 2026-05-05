from django.contrib import admin
from .models import Sintoma, Recomendacion, Consulta, Consejo, MitoVerdad

admin.site.register(Sintoma)
admin.site.register(Recomendacion)
admin.site.register(Consulta)
admin.site.register(Consejo)

@admin.register(MitoVerdad)
class MitoVerdadAdmin(admin.ModelAdmin):
    list_display = ('mito', 'verdad', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('mito', 'verdad')