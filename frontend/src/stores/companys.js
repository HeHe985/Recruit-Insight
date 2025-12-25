import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCompanyStore = defineStore('company', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const companys = ref([])
  
  // 최종 저장 데이터 구조:
  // {
  //    2024: { detail: [..], ratio: [..] },
  //    2023: { detail: [..], ratio: [..] }
  // }
  const financialData = ref({}) 
  const isLoading = ref(false)
  // const bsns_year = 2024

  // 1. 회사 리스트 검색 (기존 유지)
  const getCompanys = function(keyword = null) {
    let url = `${API_URL}/api/v1/finance/corp_list/`
    let params = {}

    if (keyword) {
      url = `${API_URL}/api/v1/finance/target_corp_list/`
      params = { corp_name: keyword }
    }

    axios({ method: 'get', url, params })
      .then(res => { companys.value = res.data })
      .catch(err => console.log(err))
  }

  // 2. 재무 데이터 가져오기
  const getFinancialData = async (corpCode) => {
    isLoading.value = true
    financialData.value = {} // 초기화
    
    // 파라미터 설정 (필요시 인자로 받도록 수정 가능)
    // const params = { 
    //   bsns_year: bsns_year, 
    //   reprt_code: '11011' 
    // }

    const targetYears = [2024, 2023, 2022]
    const promises = []

    targetYears.forEach(year => {
      const detailReq = axios({
        method: 'get',
        url: `${API_URL}/api/v1/finance/financial_detail/${corpCode}`,
        params: { 
          bsns_year: year, 
          reprt_code: '11011'
        }
      })

      const ratioReq = axios({
        method: 'get',
        url: `${API_URL}/api/v1/finance/financial_ratio/${corpCode}`,
        params: { 
          bsns_year: year, 
          reprt_code: '11011' 
        }
      })

      promises.push(detailReq.then(res => ({ type: 'detail', year, data: res.data })))
      promises.push(ratioReq.then(res => ({ type: 'ratio', year, data: res.data })))
    })

    try {
      // 병렬로 모두 실행 (가장 오래 걸리는 요청 시간만큼만 걸림)
      const results = await Promise.all(promises)

      // 받아온 데이터를 state에 예쁘게 정리
      results.forEach(item => {
        // 해당 연도 객체가 없으면 생성
        if (!financialData.value[item.year]) {
          financialData.value[item.year] = { detail: [], ratio: [] }
        }
        // 타입에 따라 데이터 저장
        financialData.value[item.year][item.type] = item.data
      })
      
      console.log('데이터 로드 완료:', financialData.value)

      } catch (err) {
        console.error('상세 데이터 조회 실패:', err)
      } finally {
        isLoading.value = false
      }
    }

    // 3. Getters (헬퍼 함수)
    // 복잡한 배열 데이터에서 원하는 값(예: 매출액)만 쏙 뽑아주는 함수
    const getAccountValue = (year, category, keyName) => {
      // category: 'detail' 또는 'ratio'
      const yearData = financialData.value[year]
      if (!yearData || !yearData[category]) return 0

      // 리스트에서 이름으로 찾기
      const found = yearData[category].find(item => {
        const name = category === 'detail' ? item.account_nm : item.ratio_nm
        // "매출액"이 포함된 항목 찾기
        return name && name.includes(keyName)
      })

      // 찾으면 숫자 반환, 없으면 0
      return found ? Number(found.thstrm_amount) : 0
    }

    return { 
      companys, 
      financialData, 
      isLoading, 
      API_URL, 
      getCompanys, 
      getFinancialData,
      getAccountValue // 뷰에서 사용하기 위해 리턴
    }
  }, { persist: true })

//     try {
//       const detailReq = axios.get(`${API_URL}/api/v1/finance/financial_detail/${corpCode}/`, { params })
//       const ratioReq = axios.get(`${API_URL}/api/v1/finance/financial_ratio/${corpCode}/`, { params })

//       const [detailRes, ratioRes] = await Promise.all([detailReq, ratioReq])

//       // 데이터 정리 함수 호출
//       organizeData(detailRes.data, 'detail')
//       organizeData(ratioRes.data, 'ratio')

//       console.log('✅ Store 저장 완료:', financialData.value)

//     } catch (err) {
//       console.error('❌ 데이터 조회 실패:', err)
//     } finally {
//       isLoading.value = false
//     }
//   }

//   // [핵심 로직] "당기, 전기" 등을 "2024, 2023" 연도별로 정리
//   const organizeData = (dataObj, type) => {
//     // dataObj 예: { "당기": [...], "전기": [...] }
//     for (const key in dataObj) {
//       const dataList = dataObj[key]

//       // ⚠️ 수정: 데이터가 1개라도 있으면 저장해야 함 (> 1 이 아니라 > 0)
//       if (dataList && dataList.length > 0) {
        
//         // 해당 리스트의 첫 번째 항목에서 '연도' 추출
//         const year = dataList[0].bsns_year

//         // 연도 키가 없으면 초기화
//         if (!financialData.value[year]) {
//           financialData.value[year] = { detail: [], ratio: [] }
//         }

//         // 데이터 저장 (detail 또는 ratio 자리에 넣기)
//         financialData.value[year][type] = dataList
//       }
//     }
//   }

//   // 3. Helper 함수: View에서 쉽게 값 꺼내쓰기 용도
//   const getAccountValue = (year, category, keyName) => {
//     // year: 2024, category: 'detail'|'ratio', keyName: '매출액'
//     const yearData = financialData.value[year]
    
//     // 데이터가 없으면 0 반환
//     if (!yearData || !yearData[category]) return 0

//     // 이름으로 찾기 (includes로 포함 여부 확인)
//     const found = yearData[category].find(item => {
//       // detail이면 account_nm, ratio면 ratio_nm (API 필드명 확인 필요)
//       const name = category === 'detail' ? item.account_nm : (item.ratio_nm || item.account_nm)
//       return name && name.includes(keyName)
//     })
    
//     // 찾으면 숫자로 변환해서 반환 (없으면 0)
//     // ⚠️ API가 문자열("1000.00")로 주므로 parseFloat 필수
//     return found ? parseFloat(found.thstrm_amount) : 0
//   }

//   return { 
//     companys, 
//     financialData, 
//     isLoading, 
//     getCompanys, 
//     getFinancialData, 
//     getAccountValue 
//   }
// }, { persist: true })