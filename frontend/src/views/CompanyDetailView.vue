<template>
  <div class="analysis-container">
    <header class="header">
      <h1>🏢 기업 재무 상세 분석</h1>
      <p>최근 3개년 ({{ targetYears.join(', ') }}) 재무제표 및 지표 분석</p>
    </header>

    <div v-if="isLoading" class="loading-state">
      데이터를 분석 중입니다... ⏳
    </div>

    <div v-else class="dashboard">
      
      <div class="charts-row">
        <div class="chart-card">
          <h3>📈 매출 및 영업이익 추이</h3>
          <div class="chart-wrapper">
            <Bar :data="growthChartData" :options="growthChartOptions" />
          </div>
        </div>
        <div class="chart-card">
          <h3>📊 주요 수익성 지표 (ROE/ROA)</h3>
          <div class="chart-wrapper">
            <Line :data="ratioChartData" :options="ratioChartOptions" />
          </div>
        </div>
      </div>

      <div class="table-card">
        <h3>📑 3개년 요약 재무제표</h3>
        <table>
          <thead>
            <tr>
              <th>구분</th>
              <th v-for="year in targetYears" :key="year">{{ year }}년</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in summaryTable" :key="item.label">
              <td class="label-col">{{ item.label }}</td>
              <td v-for="(val, idx) in item.values" :key="idx">
                {{ formatValue(val, item.unit) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Bar, Line } from 'vue-chartjs'
import { Chart as ChartJS, registerables } from 'chart.js'

ChartJS.register(...registerables)

// --- 1. 설정 및 상태 ---
const corpCode = '005930' // 예: 삼성전자 (실제 사용 시 props로 받음)
const targetYears = [2021, 2022, 2023] // 조회할 연도
const isLoading = ref(true)

// API에서 받아온 원본 데이터를 연도별로 저장할 객체
const rawData = ref({
  details: {}, // 재무제표 원본 (key: year)
  ratios: {}   // 재무비율 (key: year)
})

// --- 2. API 호출 (병렬 처리) ---
const fetchData = async () => {
  try {
    // 3년치 데이터를 동시에 호출하기 위해 Promise 배열 생성
    const promises = targetYears.map(async (year) => {
      // API 호출 시뮬레이션 (실제 axios.get으로 교체하세요)
      // const detailRes = await axios.get('/api/v1/finance/financial_detail', { params: { corp_code: corpCode, bsns_year: year, reprt_code: '11011' } })
      // const ratioRes = await axios.get('/api/v1/finance/financial_ratio', { params: { corp_code: corpCode, bsns_year: year, reprt_code: '11011' } })
      
      // 여기서는 테스트를 위해 더미 데이터를 생성합니다.
      const detailData = mockDetailApi(year)
      const ratioData = mockRatioApi(year)

      return { year, detail: detailData, ratio: ratioData }
    })

    const results = await Promise.all(promises)

    // 결과를 상태에 저장
    results.forEach(({ year, detail, ratio }) => {
      rawData.value.details[year] = detail
      rawData.value.ratios[year] = ratio
    })
    
  } catch (error) {
    console.error("데이터 로드 실패:", error)
    alert("데이터를 불러오는데 실패했습니다.")
  } finally {
    isLoading.value = false
  }
}

// --- 3. 데이터 가공 (Data Transformation) ---
// API가 주는 리스트 형태([{account_nm: '매출액', amount: 100}, ...])를 
// 우리가 필요한 값만 쏙쏙 뽑아내는 헬퍼 함수
const getValue = (year, type, keyName) => {
  const source = type === 'detail' ? rawData.value.details[year] : rawData.value.ratios[year]
  if (!source) return 0

  // API의 'account_nm'이나 'ratio_nm'에서 일치하는 항목 찾기
  const found = source.find(item => {
    const name = type === 'detail' ? item.account_nm : item.ratio_nm
    // "매출액"이 포함된 항목 찾기 (DART 데이터 특성상 공백이나 괄호가 있을 수 있음)
    return name.includes(keyName)
  })

  // 문자열로 된 숫자를 Float으로 변환 (없으면 0)
  return found ? parseFloat(found.thstrm_amount) : 0
}

// --- 4. 차트 데이터 설정 (Computed) ---

// (1) 성장성 차트 (매출 + 영업이익)
const growthChartData = computed(() => ({
  labels: targetYears.map(y => `${y}년`),
  datasets: [
    {
      type: 'bar',
      label: '매출액',
      backgroundColor: '#3b82f6',
      data: targetYears.map(y => getValue(y, 'detail', '매출액'))
    },
    {
      type: 'line',
      label: '영업이익',
      borderColor: '#ef4444',
      borderWidth: 2,
      data: targetYears.map(y => getValue(y, 'detail', '영업이익'))
    }
  ]
}))

// (2) 수익성 차트 (ROE, 부채비율)
const ratioChartData = computed(() => ({
  labels: targetYears.map(y => `${y}년`),
  datasets: [
    {
      label: 'ROE (자기자본이익률)',
      borderColor: '#10b981',
      backgroundColor: '#10b981',
      data: targetYears.map(y => getValue(y, 'ratio', 'ROE') || getValue(y, 'ratio', '자기자본이익률'))
    },
    {
      label: '부채비율',
      borderColor: '#f59e0b',
      borderDash: [5, 5], // 점선
      data: targetYears.map(y => getValue(y, 'ratio', '부채비율'))
    }
  ]
}))

// 차트 옵션
const growthChartOptions = { responsive: true, maintainAspectRatio: false }
const ratioChartOptions = { responsive: true, maintainAspectRatio: false }

// --- 5. 테이블 데이터 ---
const summaryTable = computed(() => [
  { label: '매출액', unit: 'won', values: targetYears.map(y => getValue(y, 'detail', '매출액')) },
  { label: '영업이익', unit: 'won', values: targetYears.map(y => getValue(y, 'detail', '영업이익')) },
  { label: '당기순이익', unit: 'won', values: targetYears.map(y => getValue(y, 'detail', '당기순이익')) },
  { label: '부채비율', unit: '%', values: targetYears.map(y => getValue(y, 'ratio', '부채비율')) },
  { label: 'ROE', unit: '%', values: targetYears.map(y => getValue(y, 'ratio', 'ROE')) },
])

// 숫자 포맷팅 (조/억 단위 변환 등은 여기서 커스텀)
const formatValue = (val, unit) => {
  if (unit === '%') return `${val.toFixed(2)}%`
  // 금액은 보기 좋게 억 단위로 나누거나 콤마 찍기
  return Math.toLocaleString ? Math.round(val).toLocaleString() : val
}

onMounted(() => {
  fetchData()
})

// --- (참고용) Mock Data Generators ---
const mockDetailApi = (year) => {
  const base = (year - 2000) * 1000
  return [
    { account_nm: '매출액', thstrm_amount: `${base + 5000}` },
    { account_nm: '영업이익', thstrm_amount: `${base + 500}` },
    { account_nm: '당기순이익', thstrm_amount: `${base + 300}` },
  ]
}
const mockRatioApi = (year) => {
  return [
    { ratio_nm: '부채비율', thstrm_amount: '120.5' },
    { ratio_nm: 'ROE', thstrm_amount: `${10 + (year%5)}` },
  ]
}
</script>

<style scoped>
.analysis-container { max-width: 1000px; margin: 0 auto; padding: 20px; font-family: 'Suit', sans-serif; color: #333; }
.header { text-align: center; margin-bottom: 30px; }
.charts-row { display: flex; gap: 20px; margin-bottom: 30px; }
.chart-card { flex: 1; background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; }
.chart-wrapper { height: 300px; }
.table-card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; }
table { width: 100%; border-collapse: collapse; margin-top: 15px; }
th, td { padding: 12px; text-align: right; border-bottom: 1px solid #eee; }
th { background: #f8fafc; font-weight: 600; text-align: center; }
.label-col { text-align: left; font-weight: 500; background: #fcfcfc; }
h3 { margin: 0 0 15px 0; font-size: 1.1rem; color: #1e293b; border-left: 4px solid #3b82f6; padding-left: 10px; }
</style>