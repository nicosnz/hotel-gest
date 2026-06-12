export type MetodoPago = 'EFECTIVO' | 'TARJETA' | 'TRANSFERENCIA' | 'QR'
export type EstadoReserva = 'PENDIENTE' | 'CONFIRMADA' | 'CHECKIN' | 'FINALIZADA' | 'CANCELADA'

export interface Huesped {
  id: string
  nombre: string
  apellido: string
  documento_identidad: string
  correo: string | null
  telefono: string | null
}

export interface CrearHuespedPayload {
  nombre: string
  apellido: string
  documento_identidad: string
  correo?: string
  telefono?: string
}

export interface HabitacionDisponible {
  id: string
  numero: string
  piso: number
  tipo: string
  capacidad: number
  precio_por_noche: string
}

export interface Habitacion {
  id: string
  numero: string
  piso: number
  tipo: string
  capacidad: number
  precio_por_noche: string
  estado: string
}

export interface Servicio {
  id: string
  nombre: string
  descripcion: string | null
  precio: string
  activo: boolean
}

export interface HuespedResumen {
  id: string
  nombre: string
  apellido: string
  documento_identidad: string
  es_titular: boolean
}

export interface ConsumoResumen {
  servicio_nombre: string
  cantidad: number
  precio_unitario: string
  subtotal: string
  fecha_consumo: string
}

export interface Reserva {
  id: string
  habitacion_numero: string
  estado: EstadoReserva
  fecha_checkin_esperado: string
  fecha_checkout_esperado: string
  fecha_checkin_real: string | null
  fecha_checkout_real: string | null
  observaciones: string | null
  huespedes: HuespedResumen[]
  consumos: ConsumoResumen[]
}

export interface CrearReservaPayload {
  habitacion_id: string
  fecha_checkin_esperado: string
  fecha_checkout_esperado: string
  huesped_titular_id: string
  huespedes_adicionales: string[]
  monto_adelanto: string
  metodo_pago: MetodoPago
}

export interface ReservaConfirmada {
  reserva_id: string
  estado: string
  total_estimado: string
  pago_id: string
  mensaje: string
}
