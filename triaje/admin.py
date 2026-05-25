from django.contrib import admin
from .models import Sintoma, Recomendacion, Consulta, Consejo, MitoVerdad, MedicamentoOTC

admin.site.register(Sintoma)
admin.site.register(Recomendacion)
admin.site.register(Consulta)
admin.site.register(Consejo)

@admin.register(MitoVerdad)
class MitoVerdadAdmin(admin.ModelAdmin):
    list_display = ('mito', 'verdad', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('mito', 'verdad')

@admin.register(MedicamentoOTC)
class MedicamentoOTCAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'para_que_sirve', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'para_que_sirve')