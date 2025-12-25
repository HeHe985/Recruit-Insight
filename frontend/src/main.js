import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// 데이터 보존 및 사용을 위한 플러그인

import './assets/global.css' // 👈 여기에 추가하세요!

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAccountsStore } from '@/stores/accounts'
import App from './App.vue'
import router from './router'
import axios from "axios"


// 모든 axios 요청이 실행되기 직전마다 자동 실행
axios.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access")
  // const token = localStorage.getItem("access")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

const accounts = useAccountsStore()

app.use(router)

app.mount('#app')
