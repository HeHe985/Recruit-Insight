<template>
  <div>
    <h1>Bookmark View</h1>
    <p v-if="bookmarks.length === 0">북마크한 공고가 없습니다.</p>

    <ul v-else>
      <li v-for="b in bookmarks" :key="b.id">
        <h3>
          <RouterLink
            v-if="b.emp_seqno"
            :to="{
              name: 'job_posting_detail',
              params: { id: b.emp_seqno }
            }"
          >
            {{ b.emp_wanted_title }}
          </RouterLink>
        </h3>

        <p>회사명: {{ b.emp_busi_nm }}</p>
        <p>고용형태: {{ b.emp_wanted_type_nm }}</p>
        <p>
          기간:
          {{ b.emp_wanted_stdt }} ~ {{ b.emp_wanted_endt }}
        </p>
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