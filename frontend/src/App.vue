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
       | 
      <RouterLink :to="{name: 'mypage'}">MY PAGE</RouterLink>
    </div>
    <div v-else>
      <!-- 로그인 안했을 때 -->
      <RouterLink :to="{name: 'login'}">LOGIN</RouterLink>
      | 
      <RouterLink :to="{name: 'signup'}">SIGNUP</RouterLink>
    </div>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { useAccountsStore } from '@/stores/accounts';
import { useRouter } from 'vue-router';
// import CompanySearchView from '@/components/CompanySearchView.vue'


const accounts = useAccountsStore()
const router = useRouter()

const handleLogout = function() {
  accounts.logout()
  router.push('/accounts/login')
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
