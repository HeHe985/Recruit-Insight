<template>
<div class="cl-view-container">
    
    <header class="view-header">
      <div class="header-text">
        <h2 class="title">자기소개서 리스트</h2>
      </div>

    <RouterLink :to="{ name: 'CoverLetterCreateView'}" class="btn btn-mint btn-icon">
      <span class="plus-icon">+</span> 자기소개서 추가
    </RouterLink>
    </header>
    
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