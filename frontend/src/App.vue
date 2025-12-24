<template>
  <h1>App View</h1>
  <nav>
    <RouterLink :to="{name: 'home'}">Recruit Insight</RouterLink>
     | 
    <RouterLink :to="{name: 'job_postings_list'}">채용공고</RouterLink>
     | 
     <RouterLink :to="{name: 'login'}">LOGIN</RouterLink>
  </nav>
  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router';
</script>

<style scoped>

</style>
