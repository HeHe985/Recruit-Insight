import HomeView from '@/views/HomeView.vue'
import JobPostingDetailView from '@/views/JobPostingDetailView.vue'
import JobPostingListView from '@/views/JobPostingListView.vue'
import JobPostingView from '@/views/JobPostingView.vue'
import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useAccountsStore } from '@/stores/accounts'
import SignupView from '@/views/SignupView.vue'
import MyPageView from '@/views/MyPageView.vue'
import BookmarkView from '@/views/BookmarkView.vue'

// import MyPageView from '@/views/MyPageView.vue' // 마이페이지 임시 파일
import CoverLetterListView from '@/views/CoverLetterListView.vue'
import CoverLetterDetailView from '@/views/CoverLetterDetailView.vue'
import CompanySearchView from '@/views/CompanySearchView.vue'
import CompanyDetailView from '@/views/CompanyDetailView.vue'
import CoverLetterCreateView from '@/views/CoverLetterCreateView.vue'
import CoverLetterEditView from '@/views/CoverLetterEditView.vue'
import AIRecommendationView from '@/views/AIRecommendationView.vue'

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
          path: 'detail/:id',
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
    // 자기소개서 CRUD ======================
    {
      path: '/accounts/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/search',
      name: 'CompanySearchView',
      component: CompanySearchView
    },
    {
      path: '/company/:corpCode',
      name: 'CompanyDetailView',
      component: CompanyDetailView,
      params: true
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
      children: [
        {
          path: '/bookmark/list',
          name: 'bookmark',
          component: BookmarkView
        },
        {
          path: 'cover-letters',
          name: 'CoverLetterListView',
          component : CoverLetterListView
        },
        {
          path: 'cover-letters/:id',
          name: 'CoverLetterDetailView',
          component: CoverLetterDetailView
        },      
      ],
    },
    {
      path: '/cover-letter/create',
      name: 'CoverLetterCreateView',
      component: CoverLetterCreateView
    },
    {
      path: '/cover-letter/:id/edit',
      name: 'CoverLetterEditView',
      component: CoverLetterEditView
    },
    {
      path: '/recommendations/recommend_list',
      name: 'recommend',
      component: AIRecommendationView,
      meta: { requiresAuth: true },
    },
  ],
})

// 라우터 가드, 페이지 이동 직전
router.beforeEach((to, from, next) => {
  const accounts = useAccountsStore()

  // "이동할 페이지"가 로그인이 필요하고, 현재 로그인 안했으면
  if (to.meta.requiresAuth && !accounts.isAuthenticated) {
    // 로그인으로
    alert("로그인이 필요합니다.")
    next("/accounts/login")
  } else {
    // to로
    next()
  }
})

export default router
