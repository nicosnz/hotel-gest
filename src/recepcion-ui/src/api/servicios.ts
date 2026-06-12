import { api } from './client'
import type { Servicio } from './types'

export const servicios = {
  listar: () => api.get<Servicio[]>('/servicios/'),
}
