<template>
  <div>
		<h1>Job Posting View</h1>
		<RouterView :key="$route.fullPath" />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
</script>

<style scoped>

</style>