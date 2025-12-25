<template>
  <div class="mypage-wrapper">
    <h1 class="my-page-title">마이페이지</h1>
    
    <div class="container-custom layout-grid">
        
        <aside class="sidebar">
          <nav class="ri-card menu-card">
            <div class="menu-header">메뉴</div>
            <ul class="menu-list">
              <li>
                <RouterLink :to="{name: 'bookmark'}" class="menu-item">
                  <span class="icon">📑</span> 
                  관심 채용 공고 (북마크)
                </RouterLink>
              </li>
              <li>
                <RouterLink :to="{name: 'CoverLetterListView'}" class="menu-item">
                  <span class="icon">📝</span> 
                  자기소개서 관리
                </RouterLink>
              </li>
            </ul>
          </nav>
        </aside>

        <!-- <RouterLink :to="{name: 'bookmark'}">BOOKMARK</RouterLink> -->
        <!-- <RouterLink :to="{name: 'bookmark'}">BOOKMARK</RouterLink> -->
        <!-- |  -->
        <!-- <RouterLink :to="{name: 'CoverLetterListView'}">자기소개서 리스트</RouterLink> -->
        
        <main class="main-content">
        <RouterView v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </main>

    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>

</style>