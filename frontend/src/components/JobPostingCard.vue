<template>
	<div class="job-card ri-card ri-card-hover">
		<div class="card-body">
			<RouterLink
			:to="{
				name: 'job_posting_detail',
				params: { id: job.emp_seqno }
			}"
			class="title-link"
			>
			<div class="company-name">
        {{ job.emp_busi_nm }}
      </div>
			<h3 class="job-title">{{ job.emp_wanted_title }}</h3>
			
			<div class="tags">
				<span class="badge badge-score">{{ job.emp_wanted_type_nm }}</span>
				<span class="badge badge-score">
					{{ job.emp_wanted_stdt }} ~ {{ job.emp_wanted_endt }}
				</span>
			</div>
		</RouterLink>
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