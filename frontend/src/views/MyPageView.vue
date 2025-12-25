<template>
  <div>
    <h1>My Page View</h1>
    <RouterLink :to="{name: 'bookmark'}">BOOKMARK</RouterLink>
    <!-- <RouterLink :to="{name: 'bookmark'}">BOOKMARK</RouterLink> -->
     | 
    <RouterLink :to="{name: 'CoverLetterListView'}">자기소개서 리스트</RouterLink>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>

</style>