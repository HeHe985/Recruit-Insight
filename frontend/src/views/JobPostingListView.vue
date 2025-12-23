<template>
  <div>
		<h1>Job Posting List View</h1>
		<ul>
			<li
			v-for="post in posts"
			:key="post.id"
      >
			<h3>{{ post.emp_wanted_title }}</h3>
			<p>회사명: {{ post.emp_busi_nm }}</p>
			<p>고용형태: {{ post.emp_wanted_type_nm }}</p>
			<p>기간: {{ post.emp_wanted_stdt }} ~ {{ post.emp_wanted_endt }}</p>
			</li>
		</ul>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'

const posts = ref([])

onMounted(() => {
	axios({
		method: 'get',
		url: 'http://127.0.0.1:8000/api/v1/job_postings/',
	}).then(res => {
		console.log(res.data)
		posts.value = res.data
	}).catch(err => {
		console.error(err)
	})
})
</script>

<style scoped>

</style>