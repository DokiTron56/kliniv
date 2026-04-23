from django.contrib import admin
from .models import Sintoma, Recomendacion, Consulta, Consejo

admin.site.register(Sintoma)
admin.site.register(Recomendacion)
admin.site.register(Consulta)
admin.site.register(Consejo)