from django.contrib import admin
from .models import TiposHabitaciones,Habitaciones,Empleados,Roles,Huespedes,Reservas,Servicios,Pagos,Mantenimientos,ReservaHuesped,ReservaServicio
# Register your models here.
class ReservaHuespedInline(admin.TabularInline):
    model=ReservaHuesped
    extra=1
class ReservaServicioInline(admin.TabularInline):
    model=ReservaServicio
    extra=0
@admin.register(Habitaciones)
class HabitacionesAdmin(admin.ModelAdmin):
    pass
@admin.register(TiposHabitaciones)
class TipoHabitacionesAdmin(admin.ModelAdmin):
    pass
@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    pass
@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    pass
@admin.register(Huespedes)
class HuespedesAdmin(admin.ModelAdmin):
    pass
@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    inlines=[ReservaHuespedInline,ReservaServicioInline]

@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    pass

@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    pass
@admin.register(Mantenimientos)
class MantenimientosAdmin(admin.ModelAdmin):
    pass