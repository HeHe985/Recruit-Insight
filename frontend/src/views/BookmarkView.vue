<template>
  <div>
    <h1>Bookmark View</h1>
    <ul>
      <li>
        
      </li>
    </ul>
  </div>
</template>

<script setup>
import { bookmarkListAPI } from '@/services/accounts';
import { ref, onMounted } from 'vue'

const bookmarks = ref([])

onMounted(async () => {
  const res = await bookmarkListAPI()
  bookmarks.value = res.data
})

</script>

<style scoped>

</style>