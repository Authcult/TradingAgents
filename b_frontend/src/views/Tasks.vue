<template>
  <div class="tasks-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1><el-icon><List /></el-icon> 任务列表</h1>
      <p>查看和管理所有分析任务</p>
    </div>

    <!-- 筛选和操作 -->
    <el-card shadow="hover" class="filter-card">
      <div class="filter-bar">
        <el-select v-model="filter.status" placeholder="状态筛选" clearable style="width: 150px">
          <el-option label="全部" value="" />
          <el-option label="等待中" value="pending" />
          <el-option label="进行中" value="running" />
          <el-option label="已完成" value="completed" />
          <el-option label="失败" value="failed" />
        </el-select>
        
        <el-button @click="loadTasks" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </el-card>

    <!-- 任务列表 -->
    <el-card shadow="hover">
      <el-table
        :data="tasks"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="request.symbol" label="股票代码" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.request?.symbol || '-' }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="progress" label="进度" width="180">
          <template #default="{ row }">
            <el-progress
              :percentage="row.progress"
              :status="row.status === 'completed' ? 'success' : row.status === 'failed' ? 'exception' : ''"
              :stroke-width="8"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="message" label="消息" show-overflow-tooltip />
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'completed'"
              type="primary"
              size="small"
              text
              @click="viewResult(row)"
            >
              查看结果
            </el-button>
            <el-button
              type="danger"
              size="small"
              text
              @click="deleteTask(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty v-if="!loading && tasks.length === 0" description="暂无任务" />
    </el-card>

    <!-- 结果详情弹窗 -->
    <el-dialog
      v-model="showResultDialog"
      title="分析结果"
      width="700px"
    >
      <div v-if="selectedResult" class="result-dialog">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="股票代码">
            {{ selectedResult.symbol }}
          </el-descriptions-item>
          <el-descriptions-item label="分析日期">
            {{ selectedResult.analysis_date }}
          </el-descriptions-item>
          <el-descriptions-item label="建议操作">
            <el-tag :type="getDecisionType(selectedResult.decision?.action)">
              {{ selectedResult.decision?.action || '暂无' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="置信度">
            {{ Math.round((selectedResult.decision?.confidence || 0) * 100) }}%
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="result-summary">
          <h4>决策摘要</h4>
          <p>{{ selectedResult.decision?.summary || '暂无' }}</p>
        </div>
        
        <el-collapse>
          <el-collapse-item title="技术分析" name="technical">
            <p>{{ selectedResult.decision?.technical_analysis || '暂无' }}</p>
          </el-collapse-item>
          <el-collapse-item title="基本面分析" name="fundamental">
            <p>{{ selectedResult.decision?.fundamental_analysis || '暂无' }}</p>
          </el-collapse-item>
          <el-collapse-item title="新闻情绪" name="news">
            <p>{{ selectedResult.decision?.news_sentiment || '暂无' }}</p>
          </el-collapse-item>
          <el-collapse-item title="风险评估" name="risk">
            <p>{{ selectedResult.decision?.risk_assessment || '暂无' }}</p>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/api'

const loading = ref(false)
const tasks = ref<any[]>([])
const showResultDialog = ref(false)
const selectedResult = ref<any>(null)

const filter = reactive({
  status: ''
})

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const response = await api.analysis.getTasks(filter.status || undefined)
    if (response.data?.success) {
      tasks.value = response.data.data.tasks || []
    }
  } catch (error) {
    console.error('加载任务列表失败:', error)
    ElMessage.error('加载任务列表失败')
  } finally {
    loading.value = false
  }
}

// 查看结果
const viewResult = async (task: any) => {
  try {
    const response = await api.analysis.getTaskResult(task.task_id)
    if (response.data?.success) {
      selectedResult.value = response.data.data
      showResultDialog.value = true
    }
  } catch (error) {
    ElMessage.error('获取结果失败')
  }
}

// 删除任务
const deleteTask = async (task: any) => {
  try {
    await ElMessageBox.confirm('确定要删除此任务吗？', '确认删除', {
      type: 'warning'
    })
    
    await api.analysis.deleteTask(task.task_id)
    ElMessage.success('删除成功')
    loadTasks()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 格式化时间
const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
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
    running: '进行中',
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
    HOLD: 'warning'
  }
  return map[action] || 'info'
}

// 监听筛选变化
watch(() => filter.status, () => {
  loadTasks()
})

onMounted(() => {
  loadTasks()
})
</script>

<style lang="scss" scoped>
.tasks-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
  
  h1 {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 8px;
  }
  
  p {
    margin: 0;
    color: #909399;
  }
}

.filter-card {
  margin-bottom: 16px;
  
  .filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.result-dialog {
  .result-summary {
    margin: 20px 0;
    
    h4 {
      margin: 0 0 12px;
    }
    
    p {
      line-height: 1.8;
      color: #606266;
      background: #f5f7fa;
      padding: 16px;
      border-radius: 8px;
    }
  }
}
</style>
