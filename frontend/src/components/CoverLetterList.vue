<template>
  <div>
    <h3>Cover Letter List</h3>
    <CoverLetterListItem 
      v-for="coverLetter in store.coverletters"
      :key="coverLetter.id"
      :coverLetter="coverLetter"
    />
  </div>
</template>

<script setup>
  import { useCoverLetterStore } from '@/stores/coverletters'
  import CoverLetterListItem from '@/components/CoverLetterListItem.vue'

  const store = useCoverLetterStore()
</script>

<style scoped>

</style>
