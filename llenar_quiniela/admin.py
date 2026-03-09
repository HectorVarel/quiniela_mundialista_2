from django.contrib import admin
from tabla_general.models import PI
from .models import EquiposPartidos, Prediccion, Fotos_quiniela, imagenes_cartas, Equipos_fotos, Equipos_gol, Juegos_pendientes, Equipos_tiempo, Estadisticas, Momios, Clasificados
# Register your models here.

admin.site.register(EquiposPartidos)
admin.site.register(Prediccion)
admin.site.register(Fotos_quiniela)
admin.site.register(imagenes_cartas)
admin.site.register(Equipos_gol)
admin.site.register(Equipos_fotos)
admin.site.register(Juegos_pendientes)
admin.site.register(Equipos_tiempo)
admin.site.register(Estadisticas)
admin.site.register(Momios)
admin.site.register(PI)
admin.site.register(Clasificados)