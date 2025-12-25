<template>
  <div class="bookmark-view-container">
  <header class="section-header">
    <h2 class="title">
      관심 채용 공고
    </h2>
      <span class="count" v-if="bookmarks.length > 0">{{ bookmarks.length }}개의 공고가 북마크되어 있어요!</span>
  </header>
  
    <div v-if="bookmarks.length === 0" class="empty-state">
      <h3 class="empty-title">아직 찜한 공고가 없어요!</h3>      
      <RouterLink :to="{name: 'job_postings_list'}" class="btn btn-mint">
        채용 공고를 둘러보세요!
      </RouterLink>
    </div>
    
    
    
    <div v-else class="job-grid">
      <div 
      v-for="b in bookmarks" 
      :key="b.emp_seqno || b.id" 
      class="custom-card"
      >

      <div class="job-card ri-card ri-card-hover">
      	<div class="card-body">
          <RouterLink
            :to="{
              name: 'job_posting_detail',
              params: { id: b.emp_seqno }
            }"
            class="title-link"
          >
        <p class="company-name">{{ b.emp_busi_nm }}</p>

        <h3 class="job-title">
            {{ b.emp_wanted_title }}
          </h3>
          
          <div class="tags">
            <span class="badge badge-score">{{ b.emp_wanted_type_nm }}</span>
            <span class="badge badge-score">{{ b.emp_wanted_stdt }} ~ {{ b.emp_wanted_endt }}
            </span>
          </div>
        </RouterLink>
        </div>
      </div>
    </div>
  </div>

  </div>
</template>

<script setup>
import { bookmarkListAPI } from '@/services/accounts';
import { ref, onMounted } from 'vue'

const bookmarks = ref([])

onMounted(async () => {
  const res = await bookmarkListAPI()
  bookmarks.value = res.data
})

</script>

<style scoped>

</style>