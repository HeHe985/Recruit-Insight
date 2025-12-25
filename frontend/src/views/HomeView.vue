<template>
	<div>
  	<h1>Home View</h1>

			<div class="search-section">
				<h1>회사 검색</h1>
				<div class="search-box">
					<input 
						type="text" 
						v-model="keyword" 
						@keyup.enter="search" 
						placeholder="회사명을 입력하세요"
					>
					<button @click="search">검색</button>
				</div>
		</div>


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

//검색import
import { useCompanyStore } from '@/stores/companys.js'
import { useRouter } from 'vue-router'

const jobs = ref([])

//검색
const router = useRouter()
const store = useCompanyStore()
const keyword = ref('')

// 검색 버튼 클릭 시
const search = function () {
  store.getCompanys(keyword.value)
  // 검색 페이지로 이동
  router.push({ name: 'CompanySearchView' })
}


onMounted(async () => {
	try {
		const res = await axios.get(
			"http://localhost:8000/api/v1/job_postings/recommend/"
    )
		// console.log("res.data:", res.data)
    jobs.value = res.data
  } catch (err) {
    console.error("추천 공고 조회 실패", err)
  }
})


</script>

<style scoped>

</style>