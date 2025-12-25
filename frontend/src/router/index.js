import HomeView from '@/views/HomeView.vue'
import JobPostingDetailView from '@/views/JobPostingDetailView.vue'
import JobPostingListView from '@/views/JobPostingListView.vue'
import JobPostingView from '@/views/JobPostingView.vue'
import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useAccountsStore } from '@/stores/accounts'
import SignupView from '@/views/SignupView.vue'

// import MyPageView from '@/views/MyPageView.vue' // 마이페이지 임시 파일
import CoverLetterListView from '@/views/CoverLetterListView.vue'
import CoverLetterDetailView from '@/views/CoverLetterDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/job_postings',
      name: 'job_postings',
      component: JobPostingView,
      children: [
        {
          path: '',
          name: 'job_postings_list',
          component: JobPostingListView
        },
        {
          path: ':id',
          name: 'job_posting_detail',
          component: JobPostingDetailView
        }
      ]
    },
    {
      path: '/accounts/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/accounts/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/cover-letter',
      name: 'CoverLetterListView',
      component : CoverLetterListView
    },
    {
      path: '/cover-letter/:id',
      name: 'CoverLetterDatailView',
      component: CoverLetterDetailView
    },
  ],
})

// 라우터 가드, 페이지 이동 직전
router.beforeEach((to, from, next) => {
  const accounts = useAccountsStore()

  // "이동할 페이지"가 로그인이 필요하고, 현재 로그인 안했으면
  if (to.meta.requiresAuth && !accounts.isAuthenticated) {
    // 로그인으로
    next("/accounts/login")
  } else {
    // to로
    next()
  }
})

export default router
