<template>
  <div class="dashboard">
    <!-- 欢迎区 -->
    <div class="welcome-section">
      <h1>欢迎使用 TradingAgents</h1>
      <p>多智能体 AI 股票分析平台，让 AI 分析师团队为您提供全面的投资分析</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#67c23a"><TrendCharts /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalAnalyses }}</div>
              <div class="stat-label">总分析数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#409eff"><Clock /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.runningTasks }}</div>
              <div class="stat-label">进行中的任务</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#e6a23c"><User /></el-icon>
            <div class="stat-info">
              <div class="stat-value">4</div>
              <div class="stat-label">AI 分析师</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速操作 -->
    <el-card shadow="hover" class="quick-actions-card">
      <template #header>
        <span>快速操作</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="action-item" @click="$router.push('/analysis')">
            <el-icon class="action-icon"><Document /></el-icon>
            <div class="action-text">
              <h4>单股分析</h4>
              <p>深度分析单只股票</p>
            </div>
          </div>
        </el-col>
        
        <el-col :span="8">
          <div class="action-item" @click="$router.push('/tasks')">
            <el-icon class="action-icon"><List /></el-icon>
            <div class="action-text">
              <h4>任务管理</h4>
              <p>查看分析任务列表</p>
            </div>
          </div>
        </el-col>
        
        <el-col :span="8">
          <div class="action-item" @click="$router.push('/about')">
            <el-icon class="action-icon"><Reading /></el-icon>
            <div class="action-text">
              <h4>了解更多</h4>
              <p>关于 TradingAgents</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- AI 分析师团队介绍 -->
    <el-card shadow="hover" class="analysts-card">
      <template #header>
        <span>🤖 AI 分析师团队</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6" v-for="analyst in analysts" :key="analyst.id">
          <div class="analyst-item">
            <div class="analyst-icon">{{ analyst.icon }}</div>
            <h4>{{ analyst.name }}</h4>
            <p>{{ analyst.description }}</p>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 系统状态 -->
    <el-card shadow="hover">
      <template #header>
        <span>系统状态</span>
      </template>
      
      <div class="status-content">
        <el-descriptions :column="3" border>
          <el-descriptions-item label="API 状态">
            <el-tag :type="apiStatus === 'connected' ? 'success' : 'danger'">
              {{ apiStatus === 'connected' ? '已连接' : '未连接' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="版本">v1.0.0</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ lastUpdate }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const stats = ref({
  totalAnalyses: 0,
  runningTasks: 0
})

const apiStatus = ref('disconnected')
const lastUpdate = ref('-')

const analysts = [
  {
    id: 'market',
    icon: '📈',
    name: '市场分析师',
    description: '分析技术指标和价格走势'
  },
  {
    id: 'social',
    icon: '📱',
    name: '社媒分析师',
    description: '分析社交媒体情绪'
  },
  {
    id: 'news',
    icon: '📰',
    name: '新闻分析师',
    description: '分析新闻和行业动态'
  },
  {
    id: 'fundamentals',
    icon: '📊',
    name: '基本面分析师',
    description: '分析公司财务状况'
  }
]

const checkApiStatus = async () => {
  try {
    await api.health.check()
    apiStatus.value = 'connected'
    lastUpdate.value = new Date().toLocaleString('zh-CN')
  } catch (error) {
    apiStatus.value = 'disconnected'
  }
}

const loadStats = async () => {
  try {
    const response = await api.analysis.getTasks()
    if (response.data?.data) {
      const tasks = response.data.data.tasks || []
      stats.value.totalAnalyses = tasks.length
      stats.value.runningTasks = tasks.filter((t: any) => t.status === 'running').length
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

onMounted(() => {
  checkApiStatus()
  loadStats()
})
</script>

<style lang="scss" scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  margin-bottom: 24px;
  
  h1 {
    margin-bottom: 12px;
    font-size: 28px;
  }
  
  p {
    opacity: 0.9;
    font-size: 16px;
  }
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  .stat-content {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .stat-icon {
    font-size: 40px;
  }
  
  .stat-value {
    font-size: 28px;
    font-weight: 600;
    color: #303133;
  }
  
  .stat-label {
    color: #909399;
    font-size: 14px;
  }
}

.quick-actions-card {
  margin-bottom: 24px;
  
  .action-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      background: #f5f7fa;
    }
    
    .action-icon {
      font-size: 36px;
      color: #667eea;
    }
    
    h4 {
      margin: 0 0 4px;
      color: #303133;
    }
    
    p {
      margin: 0;
      color: #909399;
      font-size: 13px;
    }
  }
}

.analysts-card {
  margin-bottom: 24px;
  
  .analyst-item {
    text-align: center;
    padding: 20px;
    
    .analyst-icon {
      font-size: 40px;
      margin-bottom: 12px;
    }
    
    h4 {
      margin: 0 0 8px;
      color: #303133;
    }
    
    p {
      margin: 0;
      color: #909399;
      font-size: 13px;
    }
  }
}
</style>
