import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const instance: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 可以在这里添加 token 等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// API 封装
export const api = {
  // 健康检查
  health: {
    check: () => instance.get('/health'),
    status: () => instance.get('/health/status'),
    ping: () => instance.get('/health/ping')
  },
  
  // 分析相关
  analysis: {
    // 提交分析任务
    submit: (data: {
      symbol: string
      analysis_date?: string
      research_depth?: number
      selected_analysts?: string[]
    }) => instance.post('/analysis/single', data),
    
    // 获取任务状态
    getTaskStatus: (taskId: string) => 
      instance.get(`/analysis/tasks/${taskId}/status`),
    
    // 获取任务结果
    getTaskResult: (taskId: string) => 
      instance.get(`/analysis/tasks/${taskId}/result`),
    
    // 获取任务列表
    getTasks: (status?: string) => 
      instance.get('/analysis/tasks', { params: { status } }),
    
    // 删除任务
    deleteTask: (taskId: string) => 
      instance.delete(`/analysis/tasks/${taskId}`),
    
    // 获取分析师列表
    getAnalysts: () => instance.get('/analysis/analysts')
  }
}

export default instance
