import { api } from './client'
import type { CrearHuespedPayload, Huesped } from './types'

export const huespedes = {
  listar: ()                         => api.get<Huesped[]>('/huespedes/'),
  crear:  (body: CrearHuespedPayload) => api.post<Huesped>('/huespedes/', body),
}
