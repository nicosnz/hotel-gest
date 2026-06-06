from django.db import models
from django.core.validators import MinValueValidator

import uuid
# Create your models here.
class TimeStampedMixin(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UUIDMixin(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    class Meta:
        abstract=True
# class Roles(UUIDMixin,TimeStampedMixin):
#     nombre=models.CharField(max_length=50,db_column="nombre",null=False,unique=True)
#     def __str__(self):
#         return self.nombre
#     class Meta:
#         managed=False
#         db_table='"content"."roles"'
#         verbose_name="Rol"
#         verbose_name_plural="Roles"
# class Empleados(UUIDMixin,TimeStampedMixin):
#     nombre=models.CharField(max_length=100,db_column="nombre",null=False)
#     apellido=models.CharField(max_length=100,db_column="apellido",null=False)
#     correo=models.EmailField(max_length=150,db_column="correo",unique=True)
#     telefono=models.CharField(max_length=20,db_column="telefono",unique=True)
#     activo = models.BooleanField(
#         default=True
#     )
#     rol=models.ForeignKey("Roles",db_column="rol_id",related_name="empleados",on_delete=models.PROTECT)
#     def __str__(self):
#         return self.nombre
#     class Meta:
#         managed=False
#         db_table='"content"."empleados"'
#         verbose_name="Empleado"
#         verbose_name_plural="Empleados"
# class Huespedes(UUIDMixin,TimeStampedMixin):
#     nombre=models.CharField(max_length=100,db_column="nombre",null=False)
#     apellido=models.CharField(max_length=100,db_column="apellido",null=False)
#     correo=models.EmailField(max_length=150,db_column="correo",unique=True)
#     telefono=models.CharField(max_length=20,db_column="telefono",unique=True)
#     documento_identidad=models.CharField(max_length=30,db_column="documento_identidad",unique=True,null=False)
#     fecha_registro = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.nombre
#     class Meta:
#         managed=False
#         db_table='"content"."huespedes"'
#         verbose_name="Huesped"
#         verbose_name_plural="Huespedes"
        
class TiposHabitaciones(UUIDMixin,TimeStampedMixin):
    nombre=models.CharField(max_length=100,db_column="nombre",null=False)
    descripcion=models.TextField(db_column="descripcion",null=True)
    capacidad=models.IntegerField(validators=[MinValueValidator(1)],db_column="capacidad",null=False)

    def __str__(self):
        return self.nombre
    class Meta:
        managed=False
        db_table='"content"."tipos_habitaciones"'
        verbose_name="Tipo Habitacion"
        verbose_name_plural="Tipos Habitaciones"
        
class Habitaciones(UUIDMixin,TimeStampedMixin):
    ESTADOS = [
        ("DISPONIBLE", "Disponible"),
        ("OCUPADA", "Ocupada"),
        ("RESERVADA", "Reservada"),
        ("MANTENIMIENTO", "Mantenimiento")
    ]
    numero=models.TextField(max_length=10,db_column="numero",null=True,unique=True)
    piso=models.IntegerField(validators=[MinValueValidator(1)],db_column="piso",null=False)
    tipo_habitacion=models.ForeignKey("TiposHabitaciones",db_column="tipo_habitacion_id",related_name="habitaciones",on_delete=models.PROTECT)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS
    )
    def __str__(self):
        return self.numero
    class Meta:
        managed=False
        db_table='"content"."habitaciones"'
        verbose_name="Habitacion"
        verbose_name_plural="Habitaciones"

# class Reservas(UUIDMixin,TimeStampedMixin):
#     ESTADOS = [
#         ("PENDIENTE", "Pendiente"),
#         ("CONFIRMADA", "Confirmada"),
#         ("CHECKIN", "Check-In"),
#         ("FINALIZADA", "Finalizada"),
#         ("CANCELADA", "Cancelada"),
#     ]
#     habitacion = models.ForeignKey(
#         "Habitaciones",
#         on_delete=models.PROTECT,
#         db_column="habitacion_id",
#         related_name="reservas"
#     )
#     fecha_reserva = models.DateTimeField(
#         auto_now_add=True
#     )
#     fecha_checkin_esperado = models.DateField(null=False)

#     fecha_checkout_esperado = models.DateField(null=False)

#     fecha_checkin_real = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     fecha_checkout_real = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     estado = models.CharField(
#         max_length=20,
#         choices=ESTADOS
#     )

#     observaciones = models.TextField(
#         null=True,
#         blank=True
#     )
#     huespedes = models.ManyToManyField(
#         "Huespedes",
#         through="ReservaHuesped",
#         related_name="reservas"
#     )
#     def __str__(self):
#         return f"Reserva {self.id}"
#     class Meta:
#         managed=False
#         db_table='"content"."reservas"'
#         verbose_name="Reserva"
#         verbose_name_plural="Reservas"
        
# class ReservaHuesped(TimeStampedMixin):

#     reserva = models.ForeignKey(
#         "Reservas",
#         on_delete=models.CASCADE,
#         db_column="reserva_id",
#         related_name="reserva_huespedes"
#     )

#     huesped = models.ForeignKey(
#         "Huespedes",
#         on_delete=models.PROTECT,
#         db_column="huesped_id",
#         related_name="reserva_huespedes"
#     )

#     es_titular = models.BooleanField(
#         default=False
#     )

    

#     class Meta:
#         managed=False
#         db_table = "content.reserva_huespedes"
#         verbose_name="Reserva Huesped"
#         verbose_name_plural="Reserva Huespedes"
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["reserva", "huesped"],
#                 name="pk_reserva_huesped"
#             )
#         ]

#     def __str__(self):
#         return f"{self.reserva_id} - {self.huesped_id}"
    
# class Pago(UUIDMixin,TimeStampedMixin):

#     CONCEPTOS = [
#         ("ADELANTO", "Adelanto"),
#         ("HOSPEDAJE", "Hospedaje"),
#         ("SERVICIO", "Servicio"),
#         ("REEMBOLSO", "Reembolso"),
#         ("PENALIZACION", "Penalización"),
#     ]

#     METODOS_PAGO = [
#         ("EFECTIVO", "Efectivo"),
#         ("TARJETA", "Tarjeta"),
#         ("TRANSFERENCIA", "Transferencia"),
#         ("QR", "QR"),
#     ]

#     ESTADOS = [
#         ("PENDIENTE", "Pendiente"),
#         ("PAGADO", "Pagado"),
#         ("REEMBOLSADO", "Reembolsado"),
#     ]

    

#     reserva = models.ForeignKey(
#         "Reserva",
#         on_delete=models.PROTECT,
#         db_column="reserva_id",
#         related_name="pagos"
#     )

#     monto = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     concepto = models.CharField(
#         max_length=30,
#         choices=CONCEPTOS
#     )

#     metodo_pago = models.CharField(
#         max_length=20,
#         choices=METODOS_PAGO
#     )

#     fecha_pago = models.DateTimeField(
#         auto_now_add=True
#     )

#     estado = models.CharField(
#         max_length=20,
#         choices=ESTADOS
#     )

    

#     class Meta:
#         db_table = "content.pagos"

#     def __str__(self):
#         return f"{self.concepto} - {self.monto}"