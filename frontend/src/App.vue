<script setup>
import { RouterLink, RouterView} from 'vue-router'
import { ref } from 'vue'

const userId = ref(1)
</script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>

  <nav>
    <RouterLink to="/">Home</RouterLink>  <!--a태그처럼 이동할 수 있도록 링크 연결-->
    <RouterLink to="/about">About</RouterLink>
    <RouterLink :to="{ name: 'user', params: { 'id' : userId }}">User Page</RouterLink>
  </nav>

  <RouterView /> 
  <!--화면 전환 영역-->
</template>

<style scoped></style>
