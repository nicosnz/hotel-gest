from django.contrib import admin
from .models import TiposHabitaciones,Habitaciones
# Register your models here.


@admin.register(Habitaciones)
class HabitacionesAdmin(admin.ModelAdmin):
    pass
@admin.register(TiposHabitaciones)
class TipoHabitacionesAdmin(admin.ModelAdmin):
    pass