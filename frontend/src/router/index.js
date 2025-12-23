import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'  // 자동완성 (..으로 되어 있으면 자동완성 되었다고 생각하면 됨)
import UserView from '@/views/UserView.vue'  // 컴포넌트 import
import UserProfile from '@/components/UserProfile.vue'
import UserPosts from '@/components/UserPosts.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path : '/user/:id',  // :id -> 다이나믹 라우트 매칭
      // name: 'user',
      component: UserView,  //import 필요
      children: [
        {
          path: '',
          name: 'user',
          component: UserProfile
        },
        {
          path: 'profile',
          name: 'profile',
          component: UserProfile,
        },
        {
          path: 'posts',
          name: 'posts',
          component: UserPosts,
        }
      ]
    }
  ],
})

export default router
