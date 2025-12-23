<template>
    <div>
        <h3>User View</h3>
        <p>{{ userId }}번 User</p>
        <RouterLink :to="{ name: 'profile' }">Profile</RouterLink>
        <RouterLink :to="{ name: 'posts' }">Posts</RouterLink>
    </div>
    <hr>
    <button @click="goHome">홈으로</button>
    <RouterView />
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, RouterLink, RouterView, useRouter } from 'vue-router'

const route = useRoute()
const userId = ref(route.params.id)

const router = useRouter()
const goHome = function () {
    router.push({ name : 'home'})
    // router.replace({ name : 'home'})
}
</script>

<style scoped>

</style>