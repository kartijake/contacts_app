import { create } from "zustand"
import axiosInstance from "../utils/axiosInstance"
import { toast } from "@/hooks/use-toast"

interface User {
  access: string
  refresh: string
  email: string
  isAuthenticated: boolean
}

interface AuthState {
  user: User
  loading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  setAccessToken: (token: string) => void
  logout: () => void
}
const useAuthStore = create<AuthState>((set) => ({
  user: {
    access: localStorage.getItem("access") || "",
    refresh: localStorage.getItem("refresh") || "",
    email: localStorage.getItem("email") || "",
    isAuthenticated: !!localStorage.getItem("access")
  },
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null })
    try {
      const response = await axiosInstance.post("/auth/login", { email, password })

      const userData = {
        access: response.data.access,
        refresh: response.data.refresh,
        email: response.data.email,
        isAuthenticated: true
      }

      set({ user: userData })

      localStorage.setItem("access", response.data.access_token)
      localStorage.setItem("refresh", response.data.refresh_token)
      localStorage.setItem("email", response.data.email)

      setTimeout(() => {
        window.location.replace("/dashboard")
      }, 50)
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      toast({
        title: "Error during login",
        description: err.response?.data?.message || "Login failed",
        variant: "destructive"
      })
      set({ error: err.response?.data?.message || "Login failed" })
    } finally {
      set({ loading: false })
    }
  },

  register: async (email, password) => {
    set({ loading: true, error: null })
    try {
      await axiosInstance.post("/auth/register", { email, password })
      const response = await axiosInstance.post("/auth/login", { email, password })

      const userData = {
        access: response.data.access,
        refresh: response.data.refresh,
        email: response.data.email,
        isAuthenticated: true
      }

      set({ user: userData })

      localStorage.setItem("access", response.data.access_token)
      localStorage.setItem("refresh", response.data.refresh_token)
      localStorage.setItem("email", response.data.email)
      setTimeout(() => {
        window.location.replace("/dashboard")
      }, 50)
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      toast({
        title: "Error during Sign Up",
        description: err.response?.data?.message || "Registration failed",
        variant: "destructive"
      })

      set({ error: err.response?.data?.message || "Registration failed" })
    } finally {
      set({ loading: false })
    }
  },
  setAccessToken: (token: string) => {
    set((state) => ({
      user: {
        ...state.user,
        access: token,
        isAuthenticated: true
      }
    }))
    localStorage.setItem("access", token)
  },

  logout: () => {
    set({
      user: {
        access: "",
        refresh: "",
        email: "",
        isAuthenticated: false
      }
    })

    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    localStorage.removeItem("email")
    setTimeout(() => {
      window.location.replace("/")
    }, 50)
  }
}))

export default useAuthStore
