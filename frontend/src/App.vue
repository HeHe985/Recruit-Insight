<template>
  <h1>App View</h1>
  <nav>
    <RouterLink :to="{name: 'home'}">Recruit Insight</RouterLink>
     | 
    <RouterLink :to="{name: 'job_postings'}">채용공고</RouterLink>
  </nav>
  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router';
</script>

<style scoped>

</style>
