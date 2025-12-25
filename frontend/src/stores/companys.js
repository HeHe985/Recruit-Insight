// stores/company.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCompanyStore = defineStore('company', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const companys = ref([])
  
  // 데이터 구조: { 2024: { detail: [...], ratio: [...] }, ... }
  const financialData = ref({}) 
  
  // 로딩 및 에러 상태 관리
  const isLoading = ref(false)
  const errorMessage = ref('') 

  // 1. 회사 리스트 검색
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

  // 2. 재무 데이터 가져오기 (병렬 요청)
  const getFinancialData = async (corpCode) => {
    isLoading.value = true
    errorMessage.value = '' // 에러 초기화
    financialData.value = {} // 데이터 초기화
    
    // 분석할 연도 설정 (필요시 동적으로 변경 가능)
    const targetYears = [2024, 2023, 2022]
    const promises = []

    targetYears.forEach(year => {
      // 재무제표 상세 (Detail) 요청
      const detailReq = axios({
        method: 'get',
        url: `${API_URL}/api/v1/finance/financial_detail/${corpCode}`,
        params: { bsns_year: year, reprt_code: '11011' }
      }).then(res => ({ type: 'detail', year, data: res.data }))

      // 재무비율 (Ratio) 요청
      const ratioReq = axios({
        method: 'get',
        url: `${API_URL}/api/v1/finance/financial_ratio/${corpCode}`,
        params: { bsns_year: year, reprt_code: '11011' }
      }).then(res => ({ type: 'ratio', year, data: res.data }))

      promises.push(detailReq)
      promises.push(ratioReq)
    })

    try {
      // 모든 요청 병렬 실행
      const results = await Promise.all(promises)

      // 받아온 데이터를 Store 상태에 저장
      results.forEach(item => {
        // 해당 연도 객체가 없으면 생성
        if (!financialData.value[item.year]) {
          financialData.value[item.year] = { detail: [], ratio: [] }
        }
        
        // ⚠️ 중요: API 데이터가 배열인지 확인하고 저장 (에러 방지)
        const safeData = Array.isArray(item.data) ? item.data : []
        financialData.value[item.year][item.type] = safeData
        
        // 디버깅용: 데이터가 비어있지 않으면 로그 출력
        if (safeData.length > 0) {
            console.log(`[${item.year} ${item.type}] 데이터 로드됨:`, safeData[0])
        }
      })
      
    } catch (err) {
      console.error('상세 데이터 조회 실패:', err)
      errorMessage.value = '데이터를 불러오는 중 오류가 발생했습니다.'
    } finally {
      isLoading.value = false
    }
  }

  // 3. Getters (헬퍼 함수) - 핵심 로직 수정됨
  // 복잡한 배열 데이터에서 원하는 값(예: 매출액, ROE)만 쏙 뽑아주는 함수
  const getAccountValue = (year, category, keyName) => {
    const yearData = financialData.value[year]

    // 1) 데이터 존재 여부 및 배열 여부 확인 (find 에러 방지)
    if (!yearData || !yearData[category] || !Array.isArray(yearData[category])) {
      return 0
    }

    // 2) 항목 찾기 (이름 필드가 다양할 수 있음)
    const found = yearData[category].find(item => {
      // API 필드명 대응: account_nm(상세), ratio_nm(비율), category_nm 등
      const name = item.account_nm || item.ratio_nm || item.category_nm || ''
      return name.includes(keyName)
    })

    if (!found) return 0

    // 3) 값 추출 (값 필드가 다양할 수 있음)
    // thstrm_amount(당기금액), ratio(비율), amount, val 등
    // 콤마(,)가 포함된 문자열일 경우 제거 후 숫자로 변환
    let rawValue = found.thstrm_amount || found.ratio || found.amount || found.val
    
    if (rawValue === undefined || rawValue === null) return 0
    
    // 문자열인 경우 콤마 제거 (예: "1,000" -> 1000)
    if (typeof rawValue === 'string') {
        rawValue = rawValue.replace(/,/g, '')
    }

    return Number(rawValue)
  }

  return { 
    companys, 
    financialData, 
    isLoading,
    errorMessage, // 뷰에서 사용하기 위해 추가
    API_URL, 
    getCompanys, 
    getFinancialData,
    getAccountValue 
  }
}, { persist: true })


// import { ref } from 'vue'
// import { defineStore } from 'pinia'
// import axios from 'axios'

// export const useCompanyStore = defineStore('company', () => {
//   const API_URL = 'http://127.0.0.1:8000'

//   const companys = ref([])
  
//   // 최종 저장 데이터 구조:
//   // {
//   //    2024: { detail: [..], ratio: [..] },
//   //    2023: { detail: [..], ratio: [..] }
//   // }
//   const financialData = ref({}) 
//   const isLoading = ref(false)
//   // const bsns_year = 2024

//   // 1. 회사 리스트 검색 (기존 유지)
//   const getCompanys = function(keyword = null) {
//     let url = `${API_URL}/api/v1/finance/corp_list/`
//     let params = {}

//     if (keyword) {
//       url = `${API_URL}/api/v1/finance/target_corp_list/`
//       params = { corp_name: keyword }
//     }

//     axios({ method: 'get', url, params })
//       .then(res => { companys.value = res.data })
//       .catch(err => console.log(err))
//   }

//   // 2. 재무 데이터 가져오기
//   const getFinancialData = async (corpCode) => {
//     isLoading.value = true
//     financialData.value = {} // 초기화
    
//     // 파라미터 설정 (필요시 인자로 받도록 수정 가능)
//     // const params = { 
//     //   bsns_year: bsns_year, 
//     //   reprt_code: '11011' 
//     // }

//     const targetYears = [2024, 2023, 2022]
//     const promises = []

//     targetYears.forEach(year => {
//       const detailReq = axios({
//         method: 'get',
//         url: `${API_URL}/api/v1/finance/financial_detail/${corpCode}`,
//         params: { 
//           bsns_year: year, 
//           reprt_code: '11011'
//         }
//       })

//       const ratioReq = axios({
//         method: 'get',
//         url: `${API_URL}/api/v1/finance/financial_ratio/${corpCode}`,
//         params: { 
//           bsns_year: year, 
//           reprt_code: '11011' 
//         }
//       })

//       promises.push(detailReq.then(res => ({ type: 'detail', year, data: res.data })))
//       promises.push(ratioReq.then(res => ({ type: 'ratio', year, data: res.data })))
//     })

//     try {
//       // 병렬로 모두 실행 (가장 오래 걸리는 요청 시간만큼만 걸림)
//       const results = await Promise.all(promises)

//       // 받아온 데이터를 state에 예쁘게 정리
//       results.forEach(item => {
//         // 해당 연도 객체가 없으면 생성
//         if (!financialData.value[item.year]) {
//           financialData.value[item.year] = { detail: [], ratio: [] }
//         }
//         // 타입에 따라 데이터 저장
//         financialData.value[item.year][item.type] = item.data
//       })
      
//       console.log('데이터 로드 완료:', financialData.value)

//       } catch (err) {
//         console.error('상세 데이터 조회 실패:', err)
//       } finally {
//         isLoading.value = false
//       }
//     }

//     // 3. Getters (헬퍼 함수)
//     // 복잡한 배열 데이터에서 원하는 값(예: 매출액)만 쏙 뽑아주는 함수
//     const getAccountValue = (year, category, keyName) => {
//       // category: 'detail' 또는 'ratio'
//       const yearData = financialData.value[year]
//       if (!yearData || !yearData[category]) return 0

//       // 리스트에서 이름으로 찾기
//       const found = yearData[category].find(item => {
//         const name = category === 'detail' ? item.account_nm : item.ratio_nm
//         // "매출액"이 포함된 항목 찾기
//         return name && name.includes(keyName)
//       })

//       // 찾으면 숫자 반환, 없으면 0
//       return found ? Number(found.thstrm_amount) : 0
//     }

//     return { 
//       companys, 
//       financialData, 
//       isLoading, 
//       API_URL, 
//       getCompanys, 
//       getFinancialData,
//       getAccountValue // 뷰에서 사용하기 위해 리턴
//     }
//   }, { persist: true })

// //     try {
// //       const detailReq = axios.get(`${API_URL}/api/v1/finance/financial_detail/${corpCode}/`, { params })
// //       const ratioReq = axios.get(`${API_URL}/api/v1/finance/financial_ratio/${corpCode}/`, { params })

// //       const [detailRes, ratioRes] = await Promise.all([detailReq, ratioReq])

// //       // 데이터 정리 함수 호출
// //       organizeData(detailRes.data, 'detail')
// //       organizeData(ratioRes.data, 'ratio')

// //       console.log('✅ Store 저장 완료:', financialData.value)

// //     } catch (err) {
// //       console.error('❌ 데이터 조회 실패:', err)
// //     } finally {
// //       isLoading.value = false
// //     }
// //   }

// //   // [핵심 로직] "당기, 전기" 등을 "2024, 2023" 연도별로 정리
// //   const organizeData = (dataObj, type) => {
// //     // dataObj 예: { "당기": [...], "전기": [...] }
// //     for (const key in dataObj) {
// //       const dataList = dataObj[key]

// //       // ⚠️ 수정: 데이터가 1개라도 있으면 저장해야 함 (> 1 이 아니라 > 0)
// //       if (dataList && dataList.length > 0) {
        
// //         // 해당 리스트의 첫 번째 항목에서 '연도' 추출
// //         const year = dataList[0].bsns_year

// //         // 연도 키가 없으면 초기화
// //         if (!financialData.value[year]) {
// //           financialData.value[year] = { detail: [], ratio: [] }
// //         }

// //         // 데이터 저장 (detail 또는 ratio 자리에 넣기)
// //         financialData.value[year][type] = dataList
// //       }
// //     }
// //   }

// //   // 3. Helper 함수: View에서 쉽게 값 꺼내쓰기 용도
// //   const getAccountValue = (year, category, keyName) => {
// //     // year: 2024, category: 'detail'|'ratio', keyName: '매출액'
// //     const yearData = financialData.value[year]
    
// //     // 데이터가 없으면 0 반환
// //     if (!yearData || !yearData[category]) return 0

// //     // 이름으로 찾기 (includes로 포함 여부 확인)
// //     const found = yearData[category].find(item => {
// //       // detail이면 account_nm, ratio면 ratio_nm (API 필드명 확인 필요)
// //       const name = category === 'detail' ? item.account_nm : (item.ratio_nm || item.account_nm)
// //       return name && name.includes(keyName)
// //     })
    
// //     // 찾으면 숫자로 변환해서 반환 (없으면 0)
// //     // ⚠️ API가 문자열("1000.00")로 주므로 parseFloat 필수
// //     return found ? parseFloat(found.thstrm_amount) : 0
// //   }

// //   return { 
// //     companys, 
// //     financialData, 
// //     isLoading, 
// //     getCompanys, 
// //     getFinancialData, 
// //     getAccountValue 
// //   }
// // }, { persist: true })