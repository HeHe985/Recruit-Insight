import axios from "axios"

export const loginAPI = (username, password) => {
  return axios.post(
    "http://localhost:8000/api/v1/accounts/login/",
    { username, password }
  )
}

export const refreshAPI = (refresh) => {
  return axios.post(
    "http://localhost:8000/api/v1/accounts/refresh/",
    { refresh }
  )
}
