<template>
  <div>
    <h1>자기소개서 리스트</h1>
    <RouterLink :to="{ name: 'CoverLetterCreateView'}">[Create]</RouterLink>
    <CoverLetterList />
  </div>
</template>

<script setup>
  import { onMounted } from 'vue'
  import { useCoverLetterStore } from '@/stores/coverletters';

  import { RouterLink } from 'vue-router'
  import CoverLetterList from '@/components/CoverLetterList.vue'

  const store = useCoverLetterStore()

  onMounted(() => {
    store.getCoverLetters()
  })
</script>

<style scoped>

</style>