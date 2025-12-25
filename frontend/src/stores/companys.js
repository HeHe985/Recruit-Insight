import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCompanyStore = defineStore('company', () => {
  const companys = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getCompanys = function() {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/finance/corp_list/`
    })
    .then(res => {
      console.log(res)
      console.log(res.data)
      companys.value = res.data
    })
    .catch(err => console.log(err))
  }

  return {companys, API_URL, getCompanys}
}, { persist : true})