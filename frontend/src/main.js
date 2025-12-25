import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAccountsStore } from '@/stores/accounts'
import App from './App.vue'
import router from './router'
import axios from "axios"


// 모든 axios 요청이 실행되기 직전마다 자동 실행
axios.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

const app = createApp(App)

app.use(createPinia())

const accounts = useAccountsStore()
app.use(router)

app.mount('#app')
