import { toast } from "@/hooks/use-toast"
import useAuthStore from "@/states/useAuthStore"
import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios"

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL as string,
  headers: {
    "Content-Type": "application/json"
  },
  withCredentials: true
})

declare module "axios" {
  export interface AxiosRequestConfig {
    _retry?: boolean
  }
}

axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }

    // 🔹 Handle 401 Unauthorized (Token Expired)
    if (error.response?.status === 401) {
      // If refresh request itself fails with 401, logout and redirect
      if (originalRequest.url?.includes("/auth/token/refresh")) {
        console.error("Refresh token request failed => Logging out user...")
        toast({ description: "Your session has expired. Please log in again." })
        useAuthStore.getState().logout()
        return Promise.reject(new Error("Session expired, please log in again."))
      }

      if (originalRequest._retry) {
        console.error("Token refresh already attempted, stopping retry.")
        return Promise.reject(error)
      }

      originalRequest._retry = true

      try {
        //  Refresh the token
        const newAccessToken = await refreshTokenRequest()
        if (!newAccessToken) throw new Error("Refresh token invalid")
        useAuthStore.getState().setAccessToken(newAccessToken)

        return axiosInstance({
          ...originalRequest,
          headers: { ...originalRequest.headers, Authorization: `Bearer ${newAccessToken}` }
        })
      } catch (refreshError) {
        console.error("Refresh token failed => logging out user...")
        useAuthStore.getState().logout()

        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

//  Refresh Token API Call
async function refreshTokenRequest() {
  const { user } = useAuthStore.getState()
  if (!user.refresh) return false

  try {
    const response = await axiosInstance.post("/auth/refresh", { refresh: user.refresh })
    return response.data.access
  } catch (error) {
    console.error("Failed to refresh token", error)
    return false
  }
}

export default axiosInstance
