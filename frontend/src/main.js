import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from "axios"

// 모든 axios 요청이 실행되기 직전마다 자동 실행
axios.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access")

  // 공개 API 목록
  const publicUrls = [
    "/api/v1/job_postings",
    "/api/v1/accounts/signup",
    "/api/v1/accounts/login",
  ]

  const isPublic = publicUrls.some((url) =>
    config.url.includes(url)
  )

  // 토큰이 있고, 퍼블릭이 아니면 
  if (token && !isPublic) {
    // 헤더에 토큰 붙이기
    config.headers.Authorization = `Bearer ${token}`
  } else {
    // 그 외에는 Authorization 헤더 제거
    delete config.headers.Authorization
  }

  return config
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
