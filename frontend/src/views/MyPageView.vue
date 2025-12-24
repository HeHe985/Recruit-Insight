<template>
  <div>
    <h1>My Page View</h1>
    <RouterLink :to="{name: 'bookmark'}">BOOKMARK</RouterLink>
    <!-- <RouterLink :to="{name: 'bookmark'}">BOOKMARK</RouterLink> -->
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>

</style>