<template>
  <div class="auth-page bg-navy">
    <div class="auth-container">

      <div class="text-center mb-8">
        <h1 class="page-title">로그인</h1>
        <p class="page-subtitle">공채 소식과 기업 분석을 한 곳에서 받아 보세요</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username" class="sr-only">아이디</label>
          <input 
            id="username"
            v-model="username" 
            type="text" 
            class="ri-input" 
            placeholder="아이디를 입력하세요" 
            required
          />    
        </div>
        <div class="form-group">>
        <label for="password" class="sr-only">비밀번호</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            class="ri-input" 
            placeholder="비밀번호를 입력하세요" 
            required
          />
        </div>
        <button type="submit" class="btn btn-mint btn-full">로그인</button>
        <p v-if="error" class="error-message">
          <span class="icon">⚠️</span> {{ error }}
        </p>
      </form>

      <div class="auth-link">
        아직 계정이 없으신가요? 
        <RouterLink :to="{name: 'signup'}" class="text-mint hover-underline">
          회원가입 하기
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAccountsStore } from "@/stores/accounts"

const username = ref("")
const password = ref("")
const error = ref("")

const accounts = useAccountsStore()
const router = useRouter()

console.log(accounts.isAuthenticated)

// const handleLogin = async () => {
//   try {
//     // console.log("username:", `"${username.value}"`)
//     // console.log("password:", `"${password.value}"`)

//     await accounts.login(username.value, password.value)
//     router.push("/")
//   } catch {
//     error.value = "아이디 또는 비밀번호가 올바르지 않습니다."
//   }
// }
const handleLogin = () => {
  accounts
    .login(username.value, password.value)
    .then(() => {
      router.push("/")
    })
    .catch(() => {
      error.value = "아이디 또는 비밀번호가 올바르지 않습니다."
    })
}
</script>



<style scoped>

</style>