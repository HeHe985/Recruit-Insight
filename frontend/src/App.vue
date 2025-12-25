<template>
  <header class="ri-header">
    <div class="container-custom header-inner">
      <div class="logo-area">
        <RouterLink :to="{name: 'home'}" class="logo-link">
          <span class="logo-text">Recruit Insight</span>
        </RouterLink>
      </div>

      <nav class="main-nav" flex-center>
      <RouterLink :to="{name: 'job_postings_list'}" class="nav-item">채용공고</RouterLink>
      | 
      <RouterLink :to="{name: 'recommend'}" class="nav-item">AI 추천</RouterLink>
      </nav>

      <div v-if="accounts.isAuthenticated" class="auth-nav">
        <!-- 로그인 했을 때 -->
        <a class="nav-item" href="#" @click.prevent="handleLogout">LOGOUT</a>
        | 
        <RouterLink :to="{name: 'mypage'}" class="nav-item">MY PAGE</RouterLink>
      </div>
      <div v-else>
        <!-- 로그인 안했을 때 -->
        <RouterLink :to="{name: 'login'}" class="nav-item">LOGIN</RouterLink>
        | 
        <RouterLink :to="{name: 'signup'}" class="nav-item">SIGNUP</RouterLink>
      </div>

    </div>
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
