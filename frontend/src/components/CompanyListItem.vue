<template>
  <div class="company-card" @click="goDetail">
    
    <div class="card-icon">
      🏢
    </div>
    
    <div class="card-info">
      <h3 class="company-name">{{ company.corp_name }}</h3>
      <p class="company-code">Code: {{ company.corp_code }}</p>
    </div>

    <div class="card-action">
      <span>분석 보기</span>
      <span class="arrow">→</span>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 부모에게 받은 회사 정보(객체)
const props = defineProps({
  company: Object
})

const goDetail = () => {
  router.push({ name: 'CompanyDetailView', params: { corpCode: props.company.corp_code } })
}

</script>

<style scoped>
  
</style>
