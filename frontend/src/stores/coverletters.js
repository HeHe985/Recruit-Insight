// 나중에 accounts에 합칠 수도 있음
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCoverLetterStore = defineStore('coverLetters', () => {
  return { }
}, { persist : true})