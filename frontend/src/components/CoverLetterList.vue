<template>
<div class="list-container">
    <div v-if="coverLetters.length > 0" class="cl-grid">
      <CoverLetterListItem 
        v-for="coverLetter in coverLetters"
        :key="coverLetter.id"
        :coverLetter="coverLetter"
      />
    </div>

    <div v-else class="empty-state">
      <p>작성된 자기소개서가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
  import { useCoverLetterStore } from '@/stores/coverletters'
  import CoverLetterListItem from '@/components/CoverLetterListItem.vue'
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  const coverLetters = ref([])
  onMounted(() => {
    axios({
      method: 'get',
      url: `http://localhost:8000/api/v1/accounts/cover_letters/`
    })
    .then((res) =>{
      console.log(res.data)
      coverLetters.value = res.data
    })
    .catch(err => console.log(err))
  })
</script>

<style scoped>

</style>
