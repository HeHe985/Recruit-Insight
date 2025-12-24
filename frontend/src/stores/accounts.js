import { defineStore } from "pinia"
import { loginAPI } from "@/services/accounts"

export const useAccountsStore = defineStore("accounts", {
  state: () => ({
    access: sessionStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
  }),

  getters: {
    isAuthenticated: (state) => !!state.access,
  },

  actions: {
    async login(username, password) {
      const res = await loginAPI(username, password)

      this.access = res.data.access
      this.refresh = res.data.refresh

      sessionStorage.setItem("access", this.access)
      localStorage.setItem("refresh", this.refresh)
    },

    logout() {
      this.access = null
      this.refresh = null

      sessionStorage.removeItem("access")
      localStorage.removeItem("refresh")
    },
  },
})
