import axios from 'axios'

export const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' },
})

// Step 141: request interceptor attaching a mock auth token
apiClient.interceptors.request.use((config) => {
  config.headers.Authorization = 'Bearer mock-token-123'
  console.log(`API call started: ${config.baseURL}${config.url}`)
  return config
})

// Step 140: response interceptor — unwrap data, standardize errors
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const statusCode = error.response?.status ?? 0
    const message = error.response?.data?.message || error.message || 'Unknown API error'
    return Promise.reject({ message, statusCode })
  }
)
