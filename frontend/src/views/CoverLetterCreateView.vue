<template>
  <div>
    <h1>자기소개서 작성</h1>
    <form @submit.prevent="createCoverLetter">
      <label for="question">자기소개서 문항 : </label>
      <input type="text" id="question" v-model.trim="question"><br>
      <label for="category">카테고리</label>
      <label for="content">답변 : </label>
      <textarea id="content" v-model.trim="content"></textarea><br>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue'

  // 드롭다운 메뉴
  const selectedOption = ref('')
  const options = ref([
    { value: '1', text: '지원동기'}
  ])
</script>

<style scoped>

</style>