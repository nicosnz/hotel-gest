import { createContext, useContext, useState, type ReactNode } from 'react'

interface AuthState {
  token: string | null
  username: string | null
  nombre: string | null
  apellido: string | null
}

interface AuthContextType {
  auth: AuthState
  login: (token: string, username: string, nombre: string, apellido: string) => void
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [auth, setAuth] = useState<AuthState>(() => ({
    token:    localStorage.getItem('token'),
    username: localStorage.getItem('username'),
    nombre:   localStorage.getItem('nombre'),
    apellido: localStorage.getItem('apellido'),
  }))

  function login(token: string, username: string, nombre: string, apellido: string) {
    localStorage.setItem('token',    token)
    localStorage.setItem('username', username)
    localStorage.setItem('nombre',   nombre)
    localStorage.setItem('apellido', apellido)
    setAuth({ token, username, nombre, apellido })
  }

  function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('nombre')
    localStorage.removeItem('apellido')
    setAuth({ token: null, username: null, nombre: null, apellido: null })
  }

  return (
    <AuthContext.Provider value={{ auth, login, logout, isAuthenticated: !!auth.token }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
