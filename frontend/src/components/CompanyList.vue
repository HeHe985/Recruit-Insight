<template>
  <div>
    <h3>회사 리스트</h3>
    <CompanyListItem 
      v-for="company in store.companys"
      :key="company.id"
      :company="company"
    />
  </div>
</template>

<script setup>
  import { useCompanyStore } from '@/stores/companys.js'
  import CompanyListItem from '@/components/CompanyListItem.vue'

  const store = useCompanyStore()
</script>

<style scoped>

</style>
