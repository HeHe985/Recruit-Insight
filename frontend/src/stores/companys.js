import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCompanyStore = defineStore('company', () => {
  const API_URL = 'http://127.0.0.1:8000'

  // 검색한 회사 리스트
  const companys = ref([])
  // 재무 정보 저장
  const financialData = ref({})
  const isLoading = ref(false)

  // [회사 검색]
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

  //[재무 데이터]
  const getFinancialData = async (cropCode) => {
    isLoading.value = true
    financialData.value = {} // 정보 초기화

    try {
      const detail = axios({
        method: 'get',
        url: `${API_URL}/api/v1/finance/financial_detail/${corpCode}/`
      })

      const ratio = axios({
        method: 'get',
        url: `${API_URL}/api/v1/finance/financial_ratio/${corpCode}/`
      })

      const [detailResponse, ratioResponse] = await Promise.all([detail, ratio])

      organizeData(detailResponse.data, 'detail')
      organizeData(ratioResponse.data, 'ratio')

      console.log('최종 저장된 데이터:', financialData.value)
    } catch (err) {
      console.error('데이터 조회 실패:', err)
    } finally{
      isLoading.value = false
    }
  }

  //   // 조회 연도
  //   const targetYear = 2024 // 나중에 입력으로 받기
  //   // 모든 API 요청 저장
  //   const promises = []

  //   // 재무제표 데이터 요청
  //   const detail = axios({
  //     method: 'get',
  //     url: `${API_URL}/api/financial_detail/<str:corp_code>/`
  //   })

  // }

  const organizeData = (dataObj, type) => {
    for (const key in dataObj) {
      const dataList = dataObj[key]

      if (dataList && dataList.length > 0) {
        // 리스트의 첫번째 아이템에서 연도를 추출
        const year = dataList[0].bsns_year

        if (!financialData.value[year]){
          financialData.value[year] = { detail: [], ratio: []}
        }

        financialData.value[year][type] = dataList
      }
    }
  }

  // Helper 함수 (View에서 사용) - 기존과 동일
  const getAccountValue = (year, category, keyName) => {
    const yearData = financialData.value[year]
    if (!yearData || !yearData[category]) return 0

    const found = yearData[category].find(item => {
      const name = category === 'detail' ? item.account_nm : item.ratio_nm
      return name && name.includes(keyName)
    })
    
    return found ? Number(found.thstrm_amount) : 0
  }

  return { 
    companys, 
    financialData, 
    isLoading, 
    getCompanys, 
    getFinancialData, 
    getAccountValue 
  }
}, { persist: true })