import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)
// Initialize Axios instance
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8080/api/v1',
  })
  
  // Set Authorization header for all requests if token exists
  const token = localStorage.getItem('token')
  if (token) {
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
  
  // Set Axios instance as a Vue prototype
  app.config.globalProperties.$http = axiosInstance
  
app.use(router)

app.mount('#app')
