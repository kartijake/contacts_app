/* eslint-disable @typescript-eslint/no-explicit-any */
import { create } from "zustand"
import axiosInstance from "@/utils/axiosInstance" // Ensure you import your custom axios instance
import useAuthStore from "./useAuthStore"
import { ContactFormData, UpdateContactFormData } from "@/pages/(protected)/dashboard/create/form"

export interface Contact {
  id: number
  user_email: string
  name: string
  address_line_1: string | null
  address_line_2: string | null
  city: string | null
  postcode: string | null
  country: string | null
  telephones: { number: string }[]
}

interface ContactState {
  contacts: Contact[]
  count: number
  page: number
  pageSize: number
  next: string | null
  previous: string | null
  loading: boolean
  error: string | null
  fetchContacts: () => Promise<void>
  searchContact: (q: string) => Promise<void>
  addContact: (formData: ContactFormData) => Promise<void>
  updateContact: (updateContact: UpdateContactFormData) => Promise<void>
  deleteContact: (id: number) => Promise<void>
  setPage: (page: number) => void
  setPageSize: (size: number) => void
}

const useContactStore = create<ContactState>((set, get) => ({
  contacts: [],
  count: 0,
  page: 1,
  pageSize: 10,
  next: null,
  previous: null,
  loading: false,
  error: null,

  fetchContacts: async () => {
    const { page, pageSize } = get()
    const url = `/contacts?page=${page}&page_size=${pageSize}`

    set({ loading: true, error: null })

    try {
      const response = await axiosInstance.get(url, {
        headers: {
          Authorization: `Bearer ${useAuthStore.getState().user.access}`
        }
      })
      const data = response.data

      set({
        contacts: data.results,
        count: data.count,
        next: data.next,
        previous: data.previous,
        loading: false
      })
    } catch (error: any) {
      set({
        error: error.response?.data?.message || "Failed to fetch contacts",
        loading: false
      })
    }
  },
  addContact: async (formData) => {
    set({ loading: true, error: null })

    try {
      await axiosInstance.post("/contacts", formData, {
        headers: {
          Authorization: `Bearer ${useAuthStore.getState().user.access}`
        }
      })
      await get().fetchContacts()
    } catch (error: any) {
      set({
        error: error.response?.data?.message || "Failed to add contact",
        loading: false
      })
    }
  },
  updateContact: async (updatedData: Partial<UpdateContactFormData>) => {
    set({ loading: true, error: null })
    try {
      await axiosInstance.put<Contact>(`/contacts/${updatedData.id}`, updatedData, {
        headers: {
          Authorization: `Bearer ${useAuthStore.getState().user.access}`
        }
      })
      await get().fetchContacts()
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || "Error updating contact"
      set({ error: errorMsg })
    } finally {
      set({ loading: false })
    }
  },
  deleteContact: async (id: number) => {
    set({ loading: true, error: null })
    try {
      await axiosInstance.delete(`/contacts/${id}`, {
        headers: {
          Authorization: `Bearer ${useAuthStore.getState().user.access}`
        }
      })
      await get().fetchContacts()
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || "Error deleting contact"
      set({ error: errorMsg })
    } finally {
      set({ loading: false })
    }
  },
  searchContact: async (q: string) => {
    set({ loading: true, error: null })
    try {
      const response = await axiosInstance.get(`/contacts/search?q=${q}`, {
        headers: {
          Authorization: `Bearer ${useAuthStore.getState().user.access}`
        }
      })
      const data = response.data

      set({
        contacts: data.results,
        count: data.count,
        next: data.next,
        previous: data.previous,
        loading: false
      })
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || "Error deleting contact"
      set({ error: errorMsg })
    } finally {
      set({ loading: false })
    }
  },

  setPage: (page) => {
    set({ page })
    get().fetchContacts()
  },

  setPageSize: (size) => {
    set({ pageSize: size, page: 1 })
    get().fetchContacts()
  }
}))

export default useContactStore
