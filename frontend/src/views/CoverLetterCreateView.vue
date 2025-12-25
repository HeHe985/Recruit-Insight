<template>
  <div>
    <h1>자기소개서 작성</h1>
    <form @submit.prevent="createCoverLetter">
      <label for="question">자기소개서 문항 : </label>
      <input type="text" id="question" v-model.trim="question"><br>
      <label for="category">카테고리</label>
      <select id="category" v-model="selectedOption">
        <option disabled value="">유형을 선택해주세요</option>
        <option v-for="option in options"
          :key="option.value"
          :value="option.value"
          >{{ option.text }}</option>
      </select>
      <label for="content">답변 : </label>
      <textarea id="content" v-model.trim="content"></textarea><br>
      <label for="note">메모 : </label>
      <textarea id="note" v-model.trim="note"></textarea>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue'

  const question = ref(null)
  // 드롭다운 메뉴
  const selectedOption = ref(null)
  const options = ref([
    { value: '1', text: '지원동기'},
    { value: '2', text: '입사 후 포부'},
    { value: '3', text: '성장 과정'},
    { value: '4', text: '성격의 장단점'},
    { value: '5', text: '직무 역량'},
    { value: '6', text: '문제 해결 경험'},
    { value: '7', text: '협업 경험'},
    { value: '8', text: '실패 경험'},
    { value: '9', text: '기타'},
  ])
  const content = ref(null)
  const note = ref(null)
</script>

<style scoped>

</style>