<template>
	<div>
  	<h1>Home View</h1>
	<h2>추천 채용 공고</h2>
		
	<div>
		<JobPostingCard
		v-for="job in jobs"
		:key="job.emp_seqno"
		:job="job"
		/>
	</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import JobPostingCard from "@/components/JobPostingCard.vue"

const jobs = ref([])

onMounted(async () => {
	try {
		const res = await axios.get(
			"http://localhost:8000/api/v1/job_postings/recommend/"
    )
		console.log("res.data:", res.data)
    jobs.value = res.data
  } catch (err) {
    console.error("추천 공고 조회 실패", err)
  }
})
</script>

<style scoped>

</style>