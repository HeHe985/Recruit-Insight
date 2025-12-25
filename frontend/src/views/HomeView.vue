<template>
	<div class="home-view">
		
		<section class="hero-section">
			<div class="container-custom hero-content">
				<h1 class="main-title"><span class="text-white">공채 소식과 </span>
					<span class="text-mint">기업 분석을 </span><br>
					동시에 제공합니다</h1>
				<p class="sub-title">
          고용 24와 DART의 정보를 모아 믿을 수 있는 정보를 제공합니다.
        </p>
				<div class="search-wrapper">
					<div class="search-box">
						<div class="search-box">
							<input 
								type="text" 
								v-model="keyword" 
								@keyup.enter="search"
								class="hero-input" 
								placeholder="회사명을 입력하세요"
							/>
							<button @click="search" class="btn btn-mint search-btn">검색</button>
						</div>
					</div>
				</div>
				</div>
			</section>

			<section class="recommend-section">
      <div class="container-custom">
        
        <div class="section-header">
          <h2 class="section-title">✨ Recruit Insight Pick</h2>
          <p class="section-desc">추천 채용 공고</p>
        </div>

				<div v-if="jobs.length > 0" class="job-grid">
					<JobPostingCard
					v-for="job in jobs"
					:key="job.emp_seqno"
					:job="job"
					/>
				</div>
			</div>
		</section>
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