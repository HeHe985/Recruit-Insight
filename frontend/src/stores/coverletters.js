// 나중에 accounts에 합칠 수도 있음
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCoverLetterStore = defineStore('coverLetter', () => {
  const coverletters = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getCoverLetters = function() {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/accounts/cover_letters/`
    })
    .then(res => {
      console.log(res)
      console.log(res.data)
      coverletters.value = res.data
    })
    .catch(err => console.log(err))
  }

  return {coverletters, API_URL, getCoverLetters}
}, { persist : true})