<template>
  <!-- <div class="company-card" @click="goDetail"> -->
    <div class="info">
      <span class="id-badge">No. {{ company.id }}</span>
      
      <h3 class="name">{{ company.corp_name }}</h3> 
    </div>
    
  <!-- </div> -->
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 부모(CompanyList)에게서 회사 정보 객체 하나를 받습니다.
const props = defineProps({
  company: Object
})

// // 클릭 시 상세 페이지로 이동
// const goDetail = () => {
//   // router/index.js 에 등록된 회사 상세 페이지 name을 적어주세요.
//   // (예: name: 'CompanyDetailView')
//   router.push({ 
//     name: 'CompanyDetailView', 
//     params: { id: props.company.id } 
//   })
// }
</script>

<style scoped>
  
</style>

<!-- <template>
  <div>
    <h4>{{ company.id }}</h4>
    <h3>{{ company.corp_name }}</h3>
    <hr>
  </div>
</template>

<script setup>

  import axios from 'axios'
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useCompanyStore } from '@/stores/companys.js'

  const store = useCompanyStore()
  const route = useRoute()
  const coverLetter = ref(null)

  defineProps({
    company: Object
  })

  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/cover_letters/${route.params.id}`
    })
    .then((res) =>{
      console.log(res.data)
      coverLetter.value = res.data
    })
    .catch(err => console.log(err))
  })
</script>

<style scoped>

</style>

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

  </div>
</template>

<script setup>
  import axios from 'axios'
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useCoverLetterStore } from '@/stores/coverletters.js'

  const store = useCoverLetterStore()
  const route = useRoute()
  const coverLetter = ref(null)

  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/cover_letters/${route.params.id}`
    })
    .then((res) =>{
      console.log(res.data)
      coverLetter.value = res.data
    })
    .catch(err => console.log(err))
  })
</script>

<style scoped>

</style> -->