from django.contrib import admin
from .models import TiposHabitaciones,Habitaciones,Empleados,Roles,Huespedes,Reservas,Servicios,Pagos,Mantenimientos,ReservaHuesped,ReservaServicio
# Register your models here.
class ReservaHuespedInline(admin.TabularInline):
    model=ReservaHuesped
    extra=1
class ReservaServicioInline(admin.TabularInline):
    model=ReservaServicio
    extra=0

class PagosInline(admin.TabularInline):
    model=Pagos
    extra=1 
@admin.register(Habitaciones)
class HabitacionesAdmin(admin.ModelAdmin):
    list_display=('numero','piso','tipo_habitacion','estado')
    search_fields=('numero',)
    
@admin.register(TiposHabitaciones)
class TipoHabitacionesAdmin(admin.ModelAdmin):
    list_display=('nombre','descripcion','capacidad')

@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    list_display=('nombre','apellido','correo','telefono','activo','rol')
    search_fields=('nombre','apellido')
    
@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    pass
@admin.register(Huespedes)
class HuespedesAdmin(admin.ModelAdmin):
    inlines=[ReservaHuespedInline]
    list_display=('nombre','apellido','correo','telefono','documento_identidad','fecha_registro')
    search_fields=('nombre','apellido')
@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    list_display=('habitacion','fecha_reserva','fecha_checkin_esperado','fecha_checkout_esperado','estado')
    inlines=[ReservaHuespedInline,ReservaServicioInline,PagosInline]
    list_filter=('estado','habitacion')

@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display=('nombre','descripcion','precio')

@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display=('reserva','concepto','monto','fecha_pago')
@admin.register(Mantenimientos)
class MantenimientosAdmin(admin.ModelAdmin):
    list_display=('habitacion','empleado','fecha_inicio','fecha_fin','estado')
