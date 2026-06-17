import { api } from './client'
import type { CrearReservaPayload, Reserva, ReservaConfirmada } from './types'

export const reservas = {
  listar: ()                          => api.get<Reserva[]>('/reservas/'),
  obtener: (id: string)               => api.get<Reserva>(`/reservas/${id}`),
  crear:   (body: CrearReservaPayload) => api.post<ReservaConfirmada>('/reservas/', body),
}
