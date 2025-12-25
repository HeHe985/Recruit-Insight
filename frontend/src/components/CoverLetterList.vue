<template>
  <div>
    <h3>Cover Letter List</h3>
    <CoverLetterListItem 
      v-for="coverLetter in coverLetters"
      :key="coverLetter.id"
      :coverLetter="coverLetter"
    />
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
