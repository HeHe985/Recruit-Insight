<template>
  <div>
    <ul>
      <li v-for="post in posts" :key="post.emp_seqno">
        <h3>
          <RouterLink
            :to="{
              name: 'job_posting_detail',
              params: { id: post.emp_seqno }
            }"
          >
            {{ post.emp_wanted_title }}
          </RouterLink>
        </h3>

        <p>회사명: {{ post.emp_busi_nm }}</p>
        <p>고용형태: {{ post.emp_wanted_type_nm }}</p>
        <p>
          기간:
          {{ post.emp_wanted_stdt }} ~ {{ post.emp_wanted_endt }}
        </p>

        <button @click="toggleBookmark(post)">
          {{ post.isBookmarked ? '북마크 삭제' : '북마크' }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, watch } from 'vue'
import { useAccountsStore } from '@/stores/accounts'
import { addBookmarkAPI, deleteBookmarkAPI } from '@/services/accounts'

const posts = ref([])
const accounts = useAccountsStore()

/* 🔹 목록 조회 (로그인 여부에 따라 Authorization 포함) */
const fetchPosts = async () => {
  const headers = {}

  if (accounts.access) {
    headers.Authorization = `Bearer ${accounts.access}`
  }

  const res = await axios.get(
    'http://127.0.0.1:8000/api/v1/job_postings/',
    { headers }
  )

  posts.value = res.data
}

/* 최초 진입 */
onMounted(fetchPosts)

/* 🔹 로그인 / 로그아웃 시 자동 재조회 */
watch(
  () => accounts.access,
  () => {
    fetchPosts()
  }
)

/* 🔹 북마크 토글 */
const toggleBookmark = async (post) => {
  const accessToken = accounts.access

  if (!accessToken) {
    alert('로그인이 필요합니다')
    return
  }

  try {
    if (post.isBookmarked) {
      await deleteBookmarkAPI(post.emp_seqno, accessToken)
    } else {
      await addBookmarkAPI(post.emp_seqno, accessToken)
    }

    // 🔥 서버 기준으로 다시 동기화
    await fetchPosts()

  } catch (err) {
    console.error(err)
    alert('북마크 처리 실패')
  }
}

</script>

<style scoped>
button {
  margin-top: 6px;
}
</style>
