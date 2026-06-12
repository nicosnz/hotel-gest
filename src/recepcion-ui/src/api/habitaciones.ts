import { api } from './client'
import type { Habitacion, HabitacionDisponible } from './types'

interface DisponibilidadResponse {
  fecha_checkin: string
  fecha_checkout: string
  noches: number
  habitaciones: HabitacionDisponible[]
  mensaje: string
}

export const habitaciones = {
  listar: () => api.get<Habitacion[]>('/habitaciones/'),
  disponibilidad: (checkin: string, checkout: string) =>
    api.get<DisponibilidadResponse>(
      `/habitaciones/disponibilidad?fecha_checkin=${checkin}&fecha_checkout=${checkout}`
    ),
}
