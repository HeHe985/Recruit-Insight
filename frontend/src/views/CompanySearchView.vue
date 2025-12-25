<template>
  <div class="search-view-container">
    <div class="header-section">
      <h1 class="page-title">기업 검색 결과</h1>
    </div>
    
    <CompanyList />
  </div>
</template>

<script setup>
  // import { useCompanyStore } from '@/stores/companys.js';

  // import { RouterLink } from 'vue-router'
  import CompanyList from '@/components/CompanyList.vue'

  // const store = useCompanyStore()

  // onMounted(() => {
  //   store.getCompanys()
  // })
</script>

<style scoped>

</style>