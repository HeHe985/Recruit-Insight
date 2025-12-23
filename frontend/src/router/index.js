import HomeView from '@/views/HomeView.vue'
import JobPostingListView from '@/views/JobPostingListView.vue'
import JobPostingView from '@/views/JobPostingView.vue'
import { createRouter, createWebHistory } from 'vue-router'

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
      component: JobPostingView,
      children: [
        {
          path: '',
          name: 'job_postings',
          component: JobPostingListView
        },
      ]
    }
  ],
})

export default router
