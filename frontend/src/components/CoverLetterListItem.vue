<template>
  <div class="cl-card" @click="goDetail">
    <RouterLink 
      :to="{name: 'CoverLetterDetailView', params: { id : coverLetter.id } }"
    >
    <div class="card-top">
      <span class="date">작성일: {{ formatDate(coverLetter.created_at) }}</span>
      <span class="id-badge">No. {{ coverLetter.id }}</span>
    </div>
    <h3 class="cl-title">
      {{ coverLetter.question }}
    </h3>
    </RouterLink>
    
  </div>
</template>

<script setup>
  import { RouterLink } from 'vue-router';
  defineProps({
    coverLetter: Object
  })

  const formatDate = (dateString) => {
    if (!dateString) return '-'
    // 서버에서 오는 날짜 형식이 ISO라면 Date 객체 변환
    const date = new Date(dateString)
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
  }
</script>

<style scoped>

</style>