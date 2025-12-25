<template>
  <div>
    <h1>자기소개서 수정</h1>
    <form @submit.prevent="updateCoverLetter">
      <label for="question">자기소개서 문항 : </label>
      <input type="text" id="question" v-model.trim="question"><br>
      <label for="category">카테고리</label>
      <select id="category" v-model="selectedOption">
        <option disabled value="">유형을 선택해주세요</option>
        <option v-for="option in options"
          :key="option.value"
          :value="option.value"
          >{{ option.text }}</option>
      </select><br>
      <label for="content">답변 : </label>
      <textarea id="content" v-model.trim="content"></textarea><br>
      <label for="note">메모 : </label>
      <textarea id="note" v-model.trim="note"></textarea><br>
      <input type="submit" text="수정완료">
    </form>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useCoverLetterStore } from '@/stores/coverletters'
  import { useRouter, useRoute } from 'vue-router'

  const question = ref(null)
  // 드롭다운 메뉴
  const selectedOption = ref(null)
  const options = ref([
    { value: '1', text: '지원동기'},
    { value: '2', text: '입사 후 포부'},
    { value: '3', text: '성장 과정'},
    { value: '4', text: '성격의 장단점'},
    { value: '5', text: '직무 역량'},
    { value: '6', text: '문제 해결 경험'},
    { value: '7', text: '협업 경험'},
    { value: '8', text: '실패 경험'},
    { value: '9', text: '기타'},
  ])
  const content = ref(null)
  const note = ref(null)

  const store = useCoverLetterStore()
  const router = useRouter()
  const route = useRoute()

  onMounted(() => {
    // 현재 글 가져오기
    const coverLetterId = route.params.id
    
    // 서버에 내용 요청
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/cover_letters/${coverLetterId}`
    })
    .then((res) => {
      // 받아 온 데이터를 변수에 넣어 보여주기
      question.value = res.data.question
      selectedOption.value = res.data.category
      content.value = res.data.content
      note.value = res.data.note
    })
    .catch(err => console.log(err))
  })


  const updateCoverLetter = function () {
    axios({
      method: 'put',
      url: `${store.API_URL}/api/v1/accounts/cover_letters/${route.params.id}/`,
      data: {
        question: question.value,
        category: selectedOption.value,
        content: content.value,
        note: note.value
      }
    })
    .then(() => {
      router.push({name: 'CoverLetterDetailView', params: { id: route.params.id }})
    })
    .catch(err => console.log(err))
  }
</script>

<style scoped>

</style>