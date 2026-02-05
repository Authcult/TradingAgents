<template>
  <div class="analysis-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1><el-icon><TrendCharts /></el-icon> 股票分析</h1>
      <p>AI 分析师团队将为您提供全面的股票分析报告</p>
    </div>

    <!-- 分析表单 -->
    <el-card shadow="hover" class="analysis-form-card">
      <template #header>
        <span>📊 分析配置</span>
      </template>
      
      <el-form :model="form" label-width="100px" class="analysis-form">
        <!-- 股票代码 -->
        <el-form-item label="股票代码" required>
          <el-input
            v-model="form.symbol"
            placeholder="输入股票代码，如 NVDA, AAPL, TSLA"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <div class="input-hint">支持美股代码（如 NVDA、AAPL）</div>
        </el-form-item>

        <!-- 分析日期 -->
        <el-form-item label="分析日期">
          <el-date-picker
            v-model="form.analysisDate"
            type="date"
            placeholder="选择分析基准日期"
            size="large"
            style="width: 100%"
            :disabled-date="disabledDate"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <!-- 分析深度 -->
        <el-form-item label="分析深度">
          <div class="depth-options">
            <div
              v-for="option in depthOptions"
              :key="option.value"
              class="depth-option"
              :class="{ active: form.researchDepth === option.value }"
              @click="form.researchDepth = option.value"
            >
              <div class="depth-icon">{{ option.icon }}</div>
              <div class="depth-info">
                <div class="depth-name">{{ option.name }}</div>
                <div class="depth-desc">{{ option.description }}</div>
              </div>
            </div>
          </div>
        </el-form-item>

        <!-- 选择分析师 -->
        <el-form-item label="分析师团队">
          <div class="analysts-grid">
            <div
              v-for="analyst in analysts"
              :key="analyst.id"
              class="analyst-item"
              :class="{ active: form.selectedAnalysts.includes(analyst.id) }"
              @click="toggleAnalyst(analyst.id)"
            >
              <span class="analyst-icon">{{ analyst.icon }}</span>
              <span class="analyst-name">{{ analyst.name }}</span>
              <el-icon v-if="form.selectedAnalysts.includes(analyst.id)" class="check-icon">
                <Check />
              </el-icon>
            </div>
          </div>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="submitting"
            :disabled="!form.symbol.trim()"
            @click="submitAnalysis"
            class="submit-btn"
          >
            <el-icon><TrendCharts /></el-icon>
            开始智能分析
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 分析进度 -->
    <el-card v-if="currentTask" shadow="hover" class="progress-card">
      <template #header>
        <div class="progress-header">
          <span>🔄 分析进行中</span>
          <el-tag :type="getStatusType(currentTask.status)">
            {{ getStatusText(currentTask.status) }}
          </el-tag>
        </div>
      </template>
      
      <div class="progress-content">
        <div class="task-info">
          <el-icon><TrendCharts /></el-icon>
          <span>{{ currentTask.symbol }}</span>
        </div>
        
        <el-progress
          :percentage="currentTask.progress"
          :status="currentTask.status === 'completed' ? 'success' : currentTask.status === 'failed' ? 'exception' : ''"
          :stroke-width="16"
        />
        
        <div class="progress-message">
          {{ currentTask.message }}
        </div>
      </div>
    </el-card>

    <!-- 分析结果 -->
    <el-card v-if="analysisResult" shadow="hover" class="result-card">
      <template #header>
        <div class="result-header">
          <span>📋 分析报告 - {{ analysisResult.symbol }}</span>
          <el-tag :type="getDecisionType(analysisResult.decision?.action)">
            {{ analysisResult.decision?.action || '暂无建议' }}
          </el-tag>
        </div>
      </template>
      
      <div class="result-content">
        <!-- 决策摘要 -->
        <div class="result-section">
          <h4><el-icon><Document /></el-icon> 决策摘要</h4>
          <div class="summary-text">
            {{ analysisResult.decision?.summary || '暂无分析摘要' }}
          </div>
          
          <div class="confidence-bar" v-if="analysisResult.decision?.confidence">
            <span>置信度</span>
            <el-progress
              :percentage="Math.round(analysisResult.decision.confidence * 100)"
              :color="getConfidenceColor(analysisResult.decision.confidence)"
            />
          </div>
        </div>

        <!-- 详细分析 -->
        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="📈 技术分析" name="technical">
            <p>{{ analysisResult.decision?.technical_analysis || '暂无技术分析' }}</p>
          </el-collapse-item>
          
          <el-collapse-item title="📊 基本面分析" name="fundamental">
            <p>{{ analysisResult.decision?.fundamental_analysis || '暂无基本面分析' }}</p>
          </el-collapse-item>
          
          <el-collapse-item title="📰 新闻情绪" name="news">
            <p>{{ analysisResult.decision?.news_sentiment || '暂无新闻分析' }}</p>
          </el-collapse-item>
          
          <el-collapse-item title="⚠️ 风险评估" name="risk">
            <p>{{ analysisResult.decision?.risk_assessment || '暂无风险评估' }}</p>
          </el-collapse-item>
        </el-collapse>

        <!-- 分析信息 -->
        <div class="analysis-meta">
          <el-descriptions :column="3" size="small" border>
            <el-descriptions-item label="分析日期">
              {{ analysisResult.analysis_date }}
            </el-descriptions-item>
            <el-descriptions-item label="研究深度">
              Lv.{{ analysisResult.research_depth }}
            </el-descriptions-item>
            <el-descriptions-item label="分析师">
              {{ analysisResult.analysts_used?.join(', ') }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/api'

// 表单数据
const form = reactive({
  symbol: '',
  analysisDate: null as string | null,
  researchDepth: 1,
  selectedAnalysts: ['market', 'news', 'fundamentals']
})

// 状态
const submitting = ref(false)
const currentTask = ref<any>(null)
const analysisResult = ref<any>(null)
const activeCollapse = ref(['technical', 'fundamental'])
let pollTimer: number | null = null

// 分析深度选项
const depthOptions = [
  { value: 1, name: '快速分析', icon: '⚡', description: '约1-2分钟' },
  { value: 2, name: '标准分析', icon: '📊', description: '约3-5分钟' },
  { value: 3, name: '深度分析', icon: '🔬', description: '约5-10分钟' }
]

// 分析师列表
const analysts = [
  { id: 'market', icon: '📈', name: '市场分析师' },
  { id: 'social', icon: '📱', name: '社媒分析师' },
  { id: 'news', icon: '📰', name: '新闻分析师' },
  { id: 'fundamentals', icon: '📊', name: '基本面分析师' }
]

// 禁用未来日期
const disabledDate = (time: Date) => {
  return time.getTime() > Date.now()
}

// 切换分析师选择
const toggleAnalyst = (id: string) => {
  const index = form.selectedAnalysts.indexOf(id)
  if (index === -1) {
    form.selectedAnalysts.push(id)
  } else if (form.selectedAnalysts.length > 1) {
    form.selectedAnalysts.splice(index, 1)
  } else {
    ElMessage.warning('至少需要选择一个分析师')
  }
}

// 获取状态类型
const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return map[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '等待中',
    running: '分析中',
    completed: '已完成',
    failed: '失败'
  }
  return map[status] || status
}

// 获取决策类型
const getDecisionType = (action: string) => {
  const map: Record<string, string> = {
    BUY: 'success',
    SELL: 'danger',
    HOLD: 'warning',
    STRONG_BUY: 'success',
    STRONG_SELL: 'danger'
  }
  return map[action] || 'info'
}

// 获取置信度颜色
const getConfidenceColor = (confidence: number) => {
  if (confidence >= 0.8) return '#67c23a'
  if (confidence >= 0.6) return '#409eff'
  if (confidence >= 0.4) return '#e6a23c'
  return '#f56c6c'
}

// 提交分析
const submitAnalysis = async () => {
  if (!form.symbol.trim()) {
    ElMessage.warning('请输入股票代码')
    return
  }

  submitting.value = true
  analysisResult.value = null

  try {
    const response = await api.analysis.submit({
      symbol: form.symbol.toUpperCase(),
      analysis_date: form.analysisDate || undefined,
      research_depth: form.researchDepth,
      selected_analysts: form.selectedAnalysts
    })

    if (response.data?.success) {
      const taskId = response.data.data.task_id
      currentTask.value = {
        taskId,
        symbol: form.symbol.toUpperCase(),
        status: 'pending',
        progress: 0,
        message: '任务已提交'
      }
      
      // 开始轮询状态
      startPolling(taskId)
      ElMessage.success('分析任务已提交')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '提交失败')
  } finally {
    submitting.value = false
  }
}

// 轮询任务状态
const startPolling = (taskId: string) => {
  if (pollTimer) clearInterval(pollTimer)
  
  pollTimer = window.setInterval(async () => {
    try {
      const statusRes = await api.analysis.getTaskStatus(taskId)
      
      if (statusRes.data?.success) {
        const data = statusRes.data.data
        currentTask.value = {
          ...currentTask.value,
          status: data.status,
          progress: data.progress,
          message: data.message
        }

        // 如果完成了，获取结果
        if (data.status === 'completed' || data.status === 'failed') {
          stopPolling()
          
          if (data.status === 'completed') {
            const resultRes = await api.analysis.getTaskResult(taskId)
            if (resultRes.data?.success) {
              analysisResult.value = resultRes.data.data
              ElMessage.success('分析完成')
            }
          } else {
            ElMessage.error('分析失败')
          }
        }
      }
    } catch (error) {
      console.error('轮询状态失败:', error)
    }
  }, 2000)
}

// 停止轮询
const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

onUnmounted(() => {
  stopPolling()
})
</script>

<style lang="scss" scoped>
.analysis-page {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
  
  h1 {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 8px;
    color: #303133;
  }
  
  p {
    margin: 0;
    color: #909399;
  }
}

.analysis-form-card {
  margin-bottom: 24px;
}

.input-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.depth-options {
  display: flex;
  gap: 16px;
  
  .depth-option {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    border: 2px solid #e4e7ed;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      border-color: #c0c4cc;
    }
    
    &.active {
      border-color: #667eea;
      background: #f0f3ff;
    }
    
    .depth-icon {
      font-size: 24px;
    }
    
    .depth-name {
      font-weight: 600;
      color: #303133;
    }
    
    .depth-desc {
      font-size: 12px;
      color: #909399;
    }
  }
}

.analysts-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  
  .analyst-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
    border: 2px solid #e4e7ed;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    position: relative;
    
    &:hover {
      border-color: #c0c4cc;
    }
    
    &.active {
      border-color: #67c23a;
      background: #f0f9eb;
    }
    
    .analyst-icon {
      font-size: 20px;
    }
    
    .analyst-name {
      font-size: 14px;
    }
    
    .check-icon {
      position: absolute;
      right: 8px;
      color: #67c23a;
    }
  }
}

.submit-btn {
  width: 200px;
  height: 48px;
  font-size: 16px;
}

.progress-card {
  margin-bottom: 24px;
  
  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .progress-content {
    .task-info {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
      font-size: 18px;
      font-weight: 600;
    }
    
    .progress-message {
      margin-top: 12px;
      color: #606266;
      text-align: center;
    }
  }
}

.result-card {
  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .result-section {
    margin-bottom: 24px;
    
    h4 {
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 0 0 12px;
    }
    
    .summary-text {
      line-height: 1.8;
      color: #606266;
      background: #f5f7fa;
      padding: 16px;
      border-radius: 8px;
    }
    
    .confidence-bar {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: 16px;
      
      span {
        white-space: nowrap;
        color: #909399;
      }
      
      .el-progress {
        flex: 1;
      }
    }
  }
  
  .analysis-meta {
    margin-top: 24px;
  }
}
</style>
