<template>
	<div>
		<h1>Job Posting Detail View</h1>
    <h1>{{ post.emp_wanted_title }}</h1>

    <p>회사명: {{ post.emp_busi_nm }} ({{ post.co_clcd_nm }})</p>
    <p>고용형태: {{ post.emp_wanted_type_nm }}</p>
    <p>
      모집기간:
      {{ post.emp_wanted_stdt }} ~ {{ post.emp_wanted_endt }}
    </p>

    <p v-if="post.recruitment_process">
      채용 절차: {{ post.recruitment_process }}
    </p>

    <hr />

    <h2>모집 직무</h2>

    <div
      v-for="job in post.jobpostingdetail_set"
      :key="job.id"
      style="margin-bottom: 24px"
    >
      <h3>{{ job.emp_recr_nm }}</h3>

      <p>근무지역: {{ job.work_region_nm }}</p>
      <p>경력: {{ job.emp_wanted_career_nm }}</p>
      <p>학력: {{ job.emp_wanted_edu_nm }}</p>

      <strong>주요 업무</strong>
      <pre>{{ job.job_cont }}</pre>

      <div v-if="job.spt_cert_etc">
        <strong>자격요건</strong>
        <pre>{{ job.spt_cert_etc }}</pre>
      </div>

      <hr />
    </div>

    <h2>지원 안내</h2>

    <p>제출 서류: {{ post.emp_submit_doc_cont }}</p>
    <p>접수 방법: {{ post.emp_rcpt_mthd_cont }}</p>

    <div v-if="post.inqry_cont">
      <strong>문의처</strong>
      <pre>{{ post.inqry_cont }}</pre>
    </div>

    <a
      v-if="post.emp_wanted_homepg_detail"
      :href="post.emp_wanted_homepg_detail"
      target="_blank"
    >
      채용 홈페이지 바로가기
    </a>
	</div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const post = ref({})

onMounted(async () => {
  const empSeqno = route.params.id

  const res = await axios.get(
    `http://127.0.0.1:8000/api/v1/job_postings/${empSeqno}/`
  )

  post.value = res.data
})
</script>

<style>

</style>