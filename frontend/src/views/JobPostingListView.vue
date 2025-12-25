<template>
  <div>
    <ul>
      <li v-for="post in posts" :key="post.emp_seqno">
        <h3>
          <RouterLink
            v-if="post.emp_seqno"
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
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const posts = ref([])

onMounted(async () => {
  const res = await axios.get("http://127.0.0.1:8000/api/v1/job_postings/")
  // console.log(res.data)
  posts.value = res.data
})

</script>

<style scoped>
</style>
