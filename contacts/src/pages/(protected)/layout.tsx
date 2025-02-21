import useAuthStore from "@/states/useAuthStore"
import React from "react"
import { Navigate } from "react-router-dom"
import Navbar from "./navbar"

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { user } = useAuthStore()
  if (user.isAuthenticated)
    return (
      <main className=' max-w-[1400px] mx-auto border-x border-dashed min-h-svh'>
        <Navbar />
        <div className='m-4'>{children}</div>
      </main>
    )
  return <Navigate to={"/"} replace />
}
