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

  <RouterLink :to="{name: 'CoverLetterListView'}">자기소개서 리스트</RouterLink>

  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { useAccountsStore } from '@/stores/accounts';
import { useRouter } from 'vue-router';

const accounts = useAccountsStore()
const router = useRouter()

const handleLogout = function() {
  accounts.logout()
  router.push('/accounts/login')
}
</script>

<style scoped>

</style>
