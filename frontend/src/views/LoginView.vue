<template>
  <div>
    <h1>Login View</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="아이디" />
      <input v-model="password" type="password" />
      <button type="submit">로그인</button>
    </form>
    <p v-if="error">{{ error }}</p>
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