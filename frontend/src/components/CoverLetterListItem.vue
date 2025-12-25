<template>
  <div>
    <h5>{{ coverLetter.id }}</h5>
    <p>{{ coverLetter.title }}</p>
    <p>{{ coverLetter.content }}</p>
    <hr>
  </div>
</template>

<script setup>
  defineProps({
    coverLetter: Object
  })
</script>

<style scoped>

</style>