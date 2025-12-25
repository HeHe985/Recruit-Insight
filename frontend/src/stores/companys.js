import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCompanyStore = defineStore('company', () => {
  const companys = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  // 검색어가 없으면 기본값
  const getCompanys = function( keyword = null ) {
    let url = `${API_URL}/api/v1/finance/corp_list/`
    let params = {}

    // 검색어가 들어온 경우
    if (keyword) {
      url = `${API_URL}/api/v1/finance/target_corp_list/`
      params = { corp_name: keyword }
    }
    console.log(url)
    console.log(params)
    axios({
      method: 'get',
      url: url,
      params: params // 검색어가 없으면 빈 객체가 들어감
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