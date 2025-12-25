<template>
	<div>
		<h1>AI Recommendation View</h1>
		<button @click="newRecommend">새로 추천 받기</button>
		<h1 v-if="loading">🔍 AI가 데이터를 분석 중입니다...</h1>
		<ul>
      <li v-for="recommend in recommends" :key="recommend.id">
        <h3>
          <RouterLink
            v-if="recommend.job_title"
            :to="{
              name: 'job_posting_detail',
              params: { id: recommend.job }
            }"
          >{{ recommend.job_title }}
          </RouterLink>
        </h3>
				<p>회사명: {{ recommend.company }}</p>
        <p>추천 이유: {{ recommend.reason }}</p>
        <p>점수: {{ recommend.score }} 점</p>
      </li>
		</ul>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { RecommendationAPI, NewRecommendAPI } from "@/services/accounts"
const loading = ref(false)
const recommends = ref([])

const fetchRecommendations = async () => {
  const res = await RecommendationAPI()
  recommends.value = res.data
}

onMounted(async () => {
  fetchRecommendations()
})

const newRecommend = async () => {
	loading.value = true
	await NewRecommendAPI()
	fetchRecommendations()
	loading.value = false
}
</script>

<style scoped>

</style>