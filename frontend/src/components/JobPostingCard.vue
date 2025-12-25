<template>
	<div class="card">
		<RouterLink
		:to="{
			name: 'job_posting_detail',
			params: { id: job.emp_seqno }
		}"
  >
		<h3 class="title">{{ job.emp_wanted_title }}</h3>
		</RouterLink>
		<p class="company">{{ job.emp_busi_nm }}</p>

		<div class="meta">
			<span class="type">{{ job.emp_wanted_type_nm }}</span>
			<span class="period">
				{{ job.emp_wanted_stdt }} ~ {{ job.emp_wanted_endt }}
			</span>
		</div>
</div>
</template>

<script setup>
import { RouterLink } from "vue-router"

const props = defineProps({
  job: {
    type: Object,
    required: true,
  },
})
</script>

<style scoped>

</style>