<template>
  <div>
    <h1>검색 결과</h1>
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