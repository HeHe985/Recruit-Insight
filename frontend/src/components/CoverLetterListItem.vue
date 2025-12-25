<template>
  <div>
    <h4>{{ coverLetter.id }}</h4>
    <h3>{{ coverLetter.question }}</h3>
    <p>작성 일자 : {{ coverLetter.created_at }}</p>
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