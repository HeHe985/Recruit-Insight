<template>
  <div>
    <h4>{{ company.id }}</h4>
    <h3>{{ company.corp_name }}</h3>
    <hr>
  </div>
</template>

<script setup>
  defineProps({
    company: Object
  })
</script>

<style scoped>

</style>