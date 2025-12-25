<template>
  <div class="analysis-container">
    <header class="header">
      <h1>기업 재무 상세 분석</h1>
      <p>최근 3개년 ({{ targetYears.join(', ') }}) 재무제표 및 지표 분석</p>
    </header>

    <div v-if="isLoading" class="loading-state">
      데이터를 분석하는 중입니다... ⏳
    </div>

    <div v-else class="dashboard">
      
      <div class="charts-row">
        <div class="chart-card">
          <h3>매출 및 영업이익 추이</h3>
          <div class="chart-wrapper">
            <Bar :data="growthChartData" :options="growthChartOptions" />
          </div>
        </div>
        <div class="chart-card">
          <h3>주요 수익성 지표 (ROE)</h3>
          <div class="chart-wrapper">
            <Line :data="ratioChartData" :options="ratioChartOptions" />
          </div>
        </div>
      </div>

      <div class="table-card">
        <h3>3개년 요약 재무제표</h3>
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
import { useRoute } from 'vue-router'
import { useCompanyStore } from '@/stores/companys.js'
import { Bar, Line } from 'vue-chartjs'
import { Chart as ChartJS, registerables } from 'chart.js'
import axios from 'axios'

ChartJS.register(...registerables)

const route = useRoute()
const store = useCompanyStore()

// --- 설정 및 상태 ---
const corpCode = route.params.corpCode
const targetYears = [2021, 2022, 2023] // 조회할 연도
const isLoading = ref(true)

onMounted(() => {
  store.getFinancialData(corpCode)
  console.log(store) // 2024년 데이터만 들어오는 것 같음
})


// --- 차트 데이터 설정 (Computed) ---

const growthChartData = computed(() => ({
  labels: targetYears.map(y => `${y}년`),
  datasets: [
    {
      type: 'bar',
      label: '매출액',
      backgroundColor: '#3b82f6',
      data: targetYears.map(y => store.getValue(y, 'detail', '매출액'))
    },
    {
      type: 'line',
      label: '영업이익',
      borderColor: '#ef4444',
      borderWidth: 2,
      data: targetYears.map(y => store.getValue(y, 'detail', '영업이익'))
    }
  ]
}))

const ratioChartData = computed(() => ({
  labels: targetYears.map(y => `${y}년`),
  datasets: [
    {
      label: 'ROE',
      borderColor: '#10b981',
      backgroundColor: '#10b981',
      data: targetYears.map(y => store.getValue(y, 'ratio', 'ROE'))
    },
    {
      label: '부채비율',
      borderColor: '#f59e0b',
      borderDash: [5, 5],
      data: targetYears.map(y => store.getValue(y, 'ratio', '부채비율'))
    }
  ]
}))

const summaryTable = computed(() => [
  { label: '매출액', unit: 'won', values: targetYears.map(y => store.getValue(y, 'detail', '매출액')) },
  { label: '영업이익', unit: 'won', values: targetYears.map(y => store.getValue(y, 'detail', '영업이익')) },
  { label: '당기순이익', unit: 'won', values: targetYears.map(y => store.getValue(y, 'detail', '당기순이익')) },
  { label: '부채비율', unit: '%', values: targetYears.map(y => store.getValue(y, 'ratio', '부채비율')) },
])

const chartOptions = { responsive: true, maintainAspectRatio: false }

const formatValue = (val, unit) => {
  if (!val) return '-'
  if (unit === '%') return `${val.toFixed(2)}%`
  return Math.round(val).toLocaleString()
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