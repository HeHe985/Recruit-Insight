<template>
  <header>
    <h1>App View</h1>
    <nav>
      <RouterLink :to="{name: 'home'}">Recruit Insight</RouterLink>
      | 
      <RouterLink :to="{name: 'job_postings_list'}">채용공고</RouterLink>
      | 
      <RouterLink :to="{name: 'login'}">LOGIN</RouterLink>
    </nav>
  </header>
  <RouterLink :to="{name: 'CoverLetterView'}">자기소개서 리스트</RouterLink>
  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router';
</script>

<style scoped>

</style>
