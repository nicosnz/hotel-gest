from enum import Enum


class EstadoHabitacion(str, Enum):
    DISPONIBLE    = "DISPONIBLE"
    OCUPADA       = "OCUPADA"
    RESERVADA     = "RESERVADA"
    MANTENIMIENTO = "MANTENIMIENTO"


class EstadoReserva(str, Enum):
    PENDIENTE  = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CHECKIN    = "CHECKIN"
    FINALIZADA = "FINALIZADA"
    CANCELADA  = "CANCELADA"


class ConceptoPago(str, Enum):
    ADELANTO     = "ADELANTO"
    HOSPEDAJE    = "HOSPEDAJE"
    SERVICIO     = "SERVICIO"
    REEMBOLSO    = "REEMBOLSO"
    PENALIZACION = "PENALIZACION"


class MetodoPago(str, Enum):
    EFECTIVO      = "EFECTIVO"
    TARJETA       = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    QR            = "QR"


class EstadoPago(str, Enum):
    PENDIENTE   = "PENDIENTE"
    PAGADO      = "PAGADO"
    REEMBOLSADO = "REEMBOLSADO"


class EstadoMantenimiento(str, Enum):
    PROGRAMADO = "PROGRAMADO"
    EN_PROCESO = "EN_PROCESO"
    FINALIZADO = "FINALIZADO"
