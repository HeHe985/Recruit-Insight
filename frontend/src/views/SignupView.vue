<template>
  <div>
    <h1>Signup View</h1>
    <form @submit.prevent="handleSignup">
      <input v-model="username">
      <input v-model="password1" type="password">
      <input v-model="password2" type="password">
      <input type="submit" value="회원가입">
    </form>
    <p v-if="error">
      {{ error }}
    </p>
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