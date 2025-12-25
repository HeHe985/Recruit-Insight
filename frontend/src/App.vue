<template>
  <header>
    <h1>App View</h1>
    <nav>
      <RouterLink :to="{name: 'home'}">Recruit Insight</RouterLink>
      | 
      <RouterLink :to="{name: 'job_postings_list'}">채용공고</RouterLink>
      | 
      <div v-if="accounts.isAuthenticated">
        <!-- 로그인 했을 때 -->
        <a href="#" @click.prevent="handleLogout">LOGOUT</a>
      </div>
      <div v-else>
        <!-- 로그인 안했을 때 -->
        <RouterLink :to="{name: 'login'}">LOGIN</RouterLink>
        | 
        <RouterLink :to="{name: 'signup'}">SIGNUP</RouterLink>
      </div>
    </nav>
  </header>
  <RouterLink :to="{name: 'CompanySearchView'}">회사 검색하기</RouterLink><br>
  <div>
    <h1>회사 검색</h1>
    <div class="search-box">
      <input 
        type="text" 
        v-model="keyword" 
        @keyup.enter="search" 
        placeholder="회사명을 입력하세요"
      >
      <button @click="search">검색</button>
    </div>
  </div>
  <RouterLink :to="{name: 'CoverLetterListView'}">자기소개서 리스트</RouterLink>

  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { useAccountsStore } from '@/stores/accounts';
import { useCompanyStore } from '@/stores/companys.js'
import { useRouter } from 'vue-router';
import { ref } from 'vue'
// import CompanySearchView from '@/components/CompanySearchView.vue'


const accounts = useAccountsStore()
const router = useRouter()

const handleLogout = function() {
  accounts.logout()
  router.push('/accounts/login')
}

//검색
const store = useCompanyStore()
const keyword = ref('')

// 검색 버튼 클릭 시
const search = function () {
  store.getCompanys(keyword.value)
  // 검색 페이지로 이동
  router.push({ name: 'CompanySearchView' })
}
</script>

<style scoped>
  /* 검색 부분 스타일 */
.search-box {
  margin: 20px 0;
}
input {
  padding: 5px;
  margin-right: 5px;
}
</style>
