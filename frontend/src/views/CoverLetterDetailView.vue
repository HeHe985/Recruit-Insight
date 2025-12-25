<template>
  <div v-if="coverLetter">
    <h3>{{ coverLetter.id }}</h3>
    <h2>{{ coverLetter.question }}</h2>
    <p>category : {{ coverLetter.category }}</p>
    <p>{{ coverLetter.content }}</p>
    <ul>
      <li>메모 : {{ coverLetter.note }}</li>
      <li>최종 수정 일자 : {{ coverLetter.updated_at }}</li>
      <li>작성 일자 : {{ coverLetter.created_at }}</li>
    </ul>
    <button @click="router.push({ name: 'CoverLetterEditView' , params: { id: route.params.id}})">수정</button>
    <button @click="deleteCoverLetter">삭제</button>
  </div>
</template>

<script setup>
  import axios from 'axios'
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useCoverLetterStore } from '@/stores/coverletters.js'

  const store = useCoverLetterStore()
  const route = useRoute()
  const router = useRouter()
  const coverLetter = ref(null)

  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/cover_letters/${route.params.id}/`
    })
    .then((res) =>{
      console.log(res.data)
      coverLetter.value = res.data
    })
    .catch(err => console.log(err))
  })

  const deleteCoverLetter = function() {
    if (confirm('정말 삭제하시겠습니까?')) {
      axios({
        method: 'delete',
        url:  `${store.API_URL}/api/v1/accounts/cover_letters/${route.params.id}/`
      })
      .then(() => {
        alert('삭제되었습니다.')
        router.push({name: 'CoverLetterListView'})
      })
      .catch((err) => console.log(err))
    }
  }
</script>

<style scoped>

</style>