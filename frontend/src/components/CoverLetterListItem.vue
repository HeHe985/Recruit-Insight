<template>
  <div>
    <h4>{{ coverLetter.id }}</h4>
    <h3>
      <RouterLink 
        :to="{name: 'CoverLetterDetailView', params: { id : coverLetter.id } }"
      >{{ coverLetter.question }}</RouterLink>
    </h3>
    <p>작성 일자 : {{ coverLetter.created_at }}</p>
    <hr>
  </div>
</template>

<script setup>
  import { RouterLink } from 'vue-router';
  defineProps({
    coverLetter: Object
  })
</script>

<style scoped>

</style>