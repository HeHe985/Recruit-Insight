<template>
  <div class="info">
    <h3 class="name">
      <RouterLink :to="{ name: 'CompanyDetailView', params: { corpCode: company.corp_code } }">
      {{ company.corp_name }}
      </RouterLink>
    </h3> 
    <hr>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 부모에게 받은 회사 정보(객체)
const props = defineProps({
  company: Object
})

</script>

<style scoped>
  
</style>
