<template>
	<div>
		<h1>AI Recommendation View</h1>
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
import { RecommendationAPI } from "@/services/accounts"

const recommends = ref([])

onMounted(async () => {
  const res = await RecommendationAPI()
  recommends.value = res.data
})
</script>

<style scoped>

</style>