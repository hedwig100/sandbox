const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

export interface Event {
  id: string
  name: string
  description: string
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  name: string
  created_at: string
  updated_at: string
}

export const api = {
  events: {
    list: async (): Promise<Event[]> => {
      const res = await fetch(`${API_BASE_URL}/events`)
      return res.json()
    },
    get: async (id: string): Promise<Event> => {
      const res = await fetch(`${API_BASE_URL}/events/${id}`)
      return res.json()
    },
    create: async (data: { name: string; description: string }): Promise<Event> => {
      const res = await fetch(`${API_BASE_URL}/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })
      return res.json()
    },
  },
  users: {
    create: async (data: { name: string }): Promise<User> => {
      const res = await fetch(`${API_BASE_URL}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })
      return res.json()
    },
  },
}
