from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from .models import TiposHabitaciones,Habitaciones,Empleados,Roles,Huespedes,Reservas,Servicios,Pagos,Mantenimientos,ReservaHuesped,ReservaServicio
# Register your models here.
class ReservaHuespedInline(TabularInline):
    model=ReservaHuesped
    extra=1
class ReservaServicioInline(TabularInline):
    model=ReservaServicio
    extra=0

class PagosInline(TabularInline):
    model=Pagos
    extra=1 
@admin.register(Habitaciones)
class HabitacionesAdmin(ModelAdmin):
    list_display=('numero','piso','tipo_habitacion','estado')
    search_fields=('numero',)
    
@admin.register(TiposHabitaciones)
class TipoHabitacionesAdmin(ModelAdmin):
    list_display=('nombre','descripcion','capacidad')

@admin.register(Empleados)
class EmpleadosAdmin(ModelAdmin):
    list_display=('nombre','apellido','correo','telefono','activo','rol')
    search_fields=('nombre','apellido')
    
@admin.register(Roles)
class RolesAdmin(ModelAdmin):
    pass
@admin.register(Huespedes)
class HuespedesAdmin(ModelAdmin):
    inlines=[ReservaHuespedInline]
    list_display=('nombre','apellido','correo','telefono','documento_identidad','fecha_registro')
    search_fields=('nombre','apellido')
@admin.register(Reservas)
class ReservasAdmin(ModelAdmin):
    list_display=('habitacion','fecha_reserva','fecha_checkin_esperado','fecha_checkout_esperado','estado')
    inlines=[ReservaHuespedInline,ReservaServicioInline,PagosInline]
    list_filter=('estado','habitacion')
    list_filter_options={
        "estado":{
            "label": ("Estado"),
            "horizontal":False
        },
        "habitacion":{
            "label": ("Habitacion"),
            "horizontal":False
        }
    }

@admin.register(Servicios)
class ServiciosAdmin(ModelAdmin):
    list_display=('nombre','descripcion','precio')

@admin.register(Pagos)
class PagosAdmin(ModelAdmin):
    list_display=('reserva','concepto','monto','fecha_pago')
@admin.register(Mantenimientos)
class MantenimientosAdmin(ModelAdmin):
    list_display=('habitacion','empleado','fecha_inicio','fecha_fin','estado')
