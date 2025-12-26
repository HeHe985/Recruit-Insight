<template>
  <div class="analysis-container">
    <header class="detail-header">
      <div class="header-top">
        <span class="badge-code" v-if="route.params.corpCode">CODE {{ route.params.corpCode }}</span>
        <h1 class="corp-name">{{ companyName }}재무 분석 리포트</h1>
      </div>
      <!-- <h1>🏢 기업 재무 상세 분석</h1> -->
      <p v-if="targetYears.length > 0">
        분석 대상: 최근 {{ targetYears.length }}개년 ({{ targetYears.join(', ') }})
      </p>
    </header>

    <div v-if="store.isLoading" class="loading-state">
      <h3>데이터를 분석하는 중입니다... ⏳</h3>
    </div>

    <div v-else-if="store.errorMessage" class="error-state">
      <h3>{{ store.errorMessage }}</h3>
    </div>

    <div v-else-if="targetYears.length === 0" class="empty-state">
      <p>표시할 데이터가 없습니다.</p>
    </div>

    <div v-else class="dashboard">
      
      <div class="charts-row">
        <div class="chart-card">
          <h3>📈 매출 및 영업이익 추이</h3>
          <div class="chart-wrapper">
            <Bar v-if="growthChartData" :data="growthChartData" :options="growthChartOptions" />
          </div>
        </div>

        <div class="chart-card">
          <h3>📊 주요 수익성 지표 (ROE/유동비율)</h3>
          <div class="chart-wrapper">
            <Line v-if="ratioChartData" :data="ratioChartData" :options="ratioChartOptions" />
          </div>
        </div>
      </div>

      <div class="table-card">
        <h3>📑 요약 재무제표</h3>
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
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCompanyStore } from '@/stores/companys.js' // 파일명 확인 (companys.js 인지 company.js 인지)

// Chart.js 관련 임포트 및 등록
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar, Line } from 'vue-chartjs'

// 차트 플러그인 등록
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const route = useRoute()
const store = useCompanyStore()


const found = store.companys.find( c => c.corp_code === route.params.corpCode)
return found ? found.corp_name : ' '


// 1. 페이지 진입 시 데이터 요청
onMounted(() => {
  if (route.params.corpCode) {
    store.getFinancialData(route.params.corpCode)
  }
})

// 2. 분석 대상 연도 계산 (Store 데이터 기반)
const targetYears = computed(() => {
  if (!store.financialData) return []
  // 키(연도)를 숫자로 바꿔서 오름차순 정렬 (예: [2022, 2023, 2024])
  return Object.keys(store.financialData).map(Number).sort((a, b) => a - b)
})

// 3. 성장성 차트 데이터 (Bar + Line 복합)
const growthChartData = computed(() => {
  if (targetYears.value.length === 0) return null

  return {
    labels: targetYears.value.map(y => `${y}년`),
    datasets: [
      {
        type: 'bar',
        label: '매출액',
        backgroundColor: '#3b82f6',
        yAxisID: 'y',
        data: targetYears.value.map(y => store.getAccountValue(y, 'detail', '매출액'))
      },
      {
        type: 'line', // 막대 그래프 위에 선 그래프 얹기
        label: '영업이익',
        borderColor: '#ef4444',
        backgroundColor: '#ef4444',
        borderWidth: 2,
        yAxisID: 'y', // 필요시 y1 축으로 분리 가능
        data: targetYears.value.map(y => store.getAccountValue(y, 'detail', '영업이익'))
      }
    ]
  }
})

// 4. 비율 차트 데이터 (Line)
const ratioChartData = computed(() => {
  if (targetYears.value.length === 0) return null

  return {
    labels: targetYears.value.map(y => `${y}년`),
    datasets: [
      {
        label: 'ROE (%)',
        borderColor: '#10b981',
        backgroundColor: '#10b981',
        tension: 0.3, // 곡선 부드럽게
        data: targetYears.value.map(y => store.getAccountValue(y, 'ratio', '자기자본순이익률')) // ratio 데이터 확인 필요
      },
      {
        label: '유동비율 (%)',
        borderColor: '#f59e0b',
        borderDash: [5, 5], // 점선
        tension: 0.3,
        data: targetYears.value.map(y => store.getAccountValue(y, 'ratio', '유동비율'))
      }
    ]
  }
})

// 5. 요약 테이블 데이터
const summaryTable = computed(() => {
  if (targetYears.value.length === 0) return []
  
  return [
    { 
      label: '매출액', 
      unit: 'won', 
      values: targetYears.value.map(y => store.getAccountValue(y, 'detail', '매출액')) 
    },
    { 
      label: '영업이익', 
      unit: 'won', 
      values: targetYears.value.map(y => store.getAccountValue(y, 'detail', '영업이익')) 
    },
    { 
      label: '당기순이익', 
      unit: 'won', 
      values: targetYears.value.map(y => store.getAccountValue(y, 'detail', '당기순이익')) 
    },
    { 
      label: '유동비율', 
      unit: '%', 
      values: targetYears.value.map(y => store.getAccountValue(y, 'ratio', '유동비율')) 
    }
  ]
})

// 6. 차트 옵션 (반응형 설정)
const commonOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
}
const growthChartOptions = { ...commonOptions }
const ratioChartOptions = { ...commonOptions }

// 7. 숫자 포맷팅 헬퍼 함수
const formatValue = (val, unit) => {
  if (val === undefined || val === null || isNaN(val)) return '-'
  
  if (unit === '%') {
    return `${val.toFixed(2)}%`
  }
  // 억 단위 등으로 나누고 싶으면 여기서 로직 추가
  // 예: return (val / 100000000).toFixed(1) + '억'
  return Math.round(val).toLocaleString() // 천단위 콤마
}
</script>

<style scoped>
/* 간단한 스타일 예시 */
.analysis-container { padding: 20px; max-width: 1200px; margin: 0 auto; }
.header { text-align: center; margin-bottom: 30px; }
.loading-state, .error-state, .empty-state { text-align: center; padding: 50px; font-size: 1.2rem; }
.error-state { color: #dc2626; }

.dashboard { display: flex; flex-direction: column; gap: 40px; }
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.chart-card, .table-card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
.chart-wrapper { height: 300px; position: relative; }

/* 테이블 스타일 */
table { width: 100%; border-collapse: collapse; margin-top: 15px; }
th, td { padding: 12px; text-align: right; border-bottom: 1px solid #e5e7eb; }
th:first-child, td:first-child { text-align: left; font-weight: bold; background-color: #f9fafb; }
th { background-color: #f3f4f6; }

/* 모바일 대응 */
@media (max-width: 768px) {
  .charts-row { grid-template-columns: 1fr; }
}
</style>