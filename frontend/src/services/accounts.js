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

export const signupAPI = (username, password1, password2) => {
  return axios.post(
    "http://localhost:8000/api/v1/accounts/signup/", {
    username,
    password1,
    password2,
  }
  )
}

export const logoutAPI = (refresh) => {
  return axios.post(
    "http://localhost:8000/api/v1/accounts/logout/",
    { refresh }
  )
}


export const bookmarkListAPI = () => {
  return axios.get(
    "http://localhost:8000/api/v1/accounts/bookmark/list/"
  )
}

export const addBookmarkAPI = (empSeqno, accessToken) => {
  return axios.post(
    `http://localhost:8000/api/v1/accounts/bookmark/${empSeqno}/`
  )
}


export const deleteBookmarkAPI = (empSeqno, accessToken) => {
  return axios.delete(
    `http://localhost:8000/api/v1/accounts/bookmark/${empSeqno}/`
  )
}


export const BookmarkListAPI = (empSeqno, accessToken) => {
  return axios.get(
    `http://localhost:8000/api/v1/accounts/bookmark/list/`
  )
}


export const RecommendationAPI = () => {
  return axios.get(
    `http://localhost:8000/api/v1/recommendations/recommend_list/`
  )
}