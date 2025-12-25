<template>
  <div>
    <div v-if="store.companys && store.companys.length > 0" class="company-grid">
      <CompanyListItem 
        v-for="company in store.companys"
        :key="company.id"
        :company="company"
      />
    </div>

    <div v-else class="no-result">
      <p>검색 결과가 없거나 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { useCompanyStore } from '@/stores/companys.js'
import CompanyListItem from '@/components/CompanyListItem.vue'

// Store를 연결만 해두면, App.vue에서 데이터를 바꿀 때마다 자동으로 화면이 바뀝니다.
const store = useCompanyStore()
</script>

<style scoped>
  
</style>
