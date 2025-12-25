<template>
  <div class="auth-page bg-navy">
    <div class="auth-container">

      <div class="text-center mb-8">
        <h1 class="page-title">회원가입</h1>
        <p class="page-subtitle">공채 소식과 기업 분석을 한 곳에서 받아 보세요</p>
      </div>

      <form @submit.prevent="handleSignup" class="signup-form">
        
        <div class="form-group">
          <label for="username" class="sr-only">아이디</label>
          <input 
            v-model="username" 
            id="username" 
            type="text" 
            class="ri-input" 
            placeholder="아이디" 
            required
          />
        </div>
        <div class="form-group">
          <label for="password" class="sr-only">비밀번호</label>
          <input 
            v-model="password1" 
            type="password"
            id="password"
            class="ri-input"
            placeholder="비밀번호"
            required
          />
        </div>
        <div class="form-group">
          <label for="password-confirm" class="sr-only">비밀번호 확인</label>
          <input 
            id="password-confirm" 
            v-model="password2" 
            type="password"
            class="ri-input" 
            placeholder="비밀번호 확인"
            required
          />
        </div>
        <p v-if="error" class="error-message">
          <span class="icon">⚠️</span> {{ error }}
        </p>
          <input class="btn btn-mint btn-full" type="submit" value="회원가입">
        </form>

        <div class="auth-link">
        이미 계정이 있으신가요? 
        <RouterLink :to="{name: 'login'}" class="text-mint hover-underline">
          로그인하기
        </RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import { signupAPI } from '@/services/accounts';
import { ref } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter()
const error = ref("")

const username = ref('')
const password1 = ref('')
const password2 = ref('')

const handleSignup = function() {
  signupAPI(username.value, password1.value, password2.value)
  .then(() => {
    router.push("/accounts/login")
  })
  .catch((err) => {
    error.value = err.response?.data?.non_field_errors?.[0] ||
      "회원가입에 실패했습니다."
  })

}
</script>

<style scoped>

</style>