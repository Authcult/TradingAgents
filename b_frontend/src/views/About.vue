<template>
  <div class="about-page">
    <!-- 项目介绍 -->
    <el-card shadow="hover" class="intro-card">
      <div class="intro-header">
        <img src="/logo.svg" alt="Logo" class="logo" />
        <h1>TradingAgents</h1>
        <p class="subtitle">多智能体 LLM 金融交易框架</p>
      </div>
      
      <div class="intro-content">
        <p>
          TradingAgents 是一个多智能体交易框架，模拟真实交易公司的运作模式。通过部署专门的 LLM 驱动智能体 —— 从基本面分析师、情绪专家、技术分析师到交易员和风险管理团队 —— 平台协作评估市场状况并做出交易决策。此外，这些智能体通过动态讨论来确定最佳策略。
        </p>
      </div>
    </el-card>

    <!-- 框架架构 -->
    <el-card shadow="hover">
      <template #header>
        <span>🏗️ 框架架构</span>
      </template>
      
      <el-row :gutter="20">
        <!-- 分析师团队 -->
        <el-col :span="12">
          <div class="team-section">
            <h3>📊 分析师团队</h3>
            <div class="team-members">
              <div class="member-item">
                <span class="member-icon">📈</span>
                <div class="member-info">
                  <h4>基本面分析师</h4>
                  <p>评估公司财务和绩效指标，识别内在价值和潜在风险</p>
                </div>
              </div>
              
              <div class="member-item">
                <span class="member-icon">📱</span>
                <div class="member-info">
                  <h4>情绪分析师</h4>
                  <p>使用情绪评分算法分析社交媒体和公众情绪</p>
                </div>
              </div>
              
              <div class="member-item">
                <span class="member-icon">📰</span>
                <div class="member-info">
                  <h4>新闻分析师</h4>
                  <p>监控全球新闻和宏观经济指标，解读事件对市场的影响</p>
                </div>
              </div>
              
              <div class="member-item">
                <span class="member-icon">📉</span>
                <div class="member-info">
                  <h4>技术分析师</h4>
                  <p>利用技术指标（如MACD和RSI）检测交易模式和预测价格走势</p>
                </div>
              </div>
            </div>
          </div>
        </el-col>
        
        <!-- 研究团队 -->
        <el-col :span="12">
          <div class="team-section">
            <h3>🔬 研究团队</h3>
            <div class="team-members">
              <div class="member-item">
                <span class="member-icon">🐂</span>
                <div class="member-info">
                  <h4>多头研究员</h4>
                  <p>从乐观角度评估市场机会和潜在收益</p>
                </div>
              </div>
              
              <div class="member-item">
                <span class="member-icon">🐻</span>
                <div class="member-info">
                  <h4>空头研究员</h4>
                  <p>从谨慎角度评估风险因素和潜在损失</p>
                </div>
              </div>
            </div>
            
            <h3 style="margin-top: 24px">💼 交易员</h3>
            <div class="team-members">
              <div class="member-item">
                <span class="member-icon">🎯</span>
                <div class="member-info">
                  <h4>交易智能体</h4>
                  <p>整合分析师和研究员的报告，做出交易决策，确定交易时机和规模</p>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 技术栈 -->
    <el-card shadow="hover">
      <template #header>
        <span>🛠️ 技术栈</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="tech-item">
            <h4>后端</h4>
            <el-tag>Python</el-tag>
            <el-tag>FastAPI</el-tag>
            <el-tag>LangChain</el-tag>
            <el-tag>LangGraph</el-tag>
          </div>
        </el-col>
        
        <el-col :span="8">
          <div class="tech-item">
            <h4>前端</h4>
            <el-tag>Vue 3</el-tag>
            <el-tag>TypeScript</el-tag>
            <el-tag>Element Plus</el-tag>
            <el-tag>Vite</el-tag>
          </div>
        </el-col>
        
        <el-col :span="8">
          <div class="tech-item">
            <h4>AI/LLM</h4>
            <el-tag>OpenAI</el-tag>
            <el-tag>Anthropic</el-tag>
            <el-tag>ModelScope</el-tag>
            <el-tag>Qwen</el-tag>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 声明 -->
    <el-card shadow="hover">
      <template #header>
        <span>⚠️ 重要声明</span>
      </template>
      
      <el-alert
        title="投资风险提示"
        type="warning"
        :closable="false"
        show-icon
      >
        <template #default>
          <p style="line-height: 1.8">
            TradingAgents 框架仅供研究和学习目的。交易表现可能因多种因素而异，包括所选的底层语言模型、模型温度、交易周期、数据质量和其他非确定性因素。
            <strong>本软件不构成财务、投资或交易建议。</strong>
            投资有风险，入市需谨慎。
          </p>
        </template>
      </el-alert>
    </el-card>

    <!-- 链接 -->
    <el-card shadow="hover">
      <template #header>
        <span>🔗 相关链接</span>
      </template>
      
      <div class="links">
        <el-button
          type="primary"
          plain
          @click="openLink('https://github.com/TauricResearch/TradingAgents')"
        >
          <el-icon><Link /></el-icon>
          GitHub
        </el-button>
        
        <el-button
          plain
          @click="openLink('https://arxiv.org/abs/2412.20138')"
        >
          <el-icon><Document /></el-icon>
          论文 (arXiv)
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
const openLink = (url: string) => {
  window.open(url, '_blank')
}
</script>

<style lang="scss" scoped>
.about-page {
  max-width: 1000px;
  margin: 0 auto;
  
  .el-card {
    margin-bottom: 24px;
  }
}

.intro-card {
  .intro-header {
    text-align: center;
    padding: 40px 20px;
    
    .logo {
      width: 80px;
      height: 80px;
      margin-bottom: 16px;
    }
    
    h1 {
      margin: 0 0 8px;
      font-size: 32px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
      margin: 0;
      color: #909399;
      font-size: 16px;
    }
  }
  
  .intro-content {
    padding: 0 20px 20px;
    
    p {
      line-height: 1.8;
      color: #606266;
      text-align: justify;
    }
  }
}

.team-section {
  h3 {
    margin: 0 0 16px;
    color: #303133;
  }
  
  .team-members {
    .member-item {
      display: flex;
      gap: 12px;
      padding: 12px;
      border-radius: 8px;
      transition: background 0.3s;
      
      &:hover {
        background: #f5f7fa;
      }
      
      .member-icon {
        font-size: 28px;
      }
      
      .member-info {
        h4 {
          margin: 0 0 4px;
          font-size: 14px;
          color: #303133;
        }
        
        p {
          margin: 0;
          font-size: 13px;
          color: #909399;
        }
      }
    }
  }
}

.tech-item {
  h4 {
    margin: 0 0 12px;
    color: #303133;
  }
  
  .el-tag {
    margin: 0 8px 8px 0;
  }
}

.links {
  display: flex;
  gap: 16px;
}
</style>
