<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <h1>校园活动发布平台</h1>
        <div style="display: flex; gap: 12px; align-items: center;">
          <span v-if="currentUser" style="margin-right: 8px;">欢迎, {{ currentUser.username }}</span>
          <button class="btn" :class="currentUser ? 'btn-outline' : 'btn-outline'" @click="currentUser ? logout() : showAuthModal = true">
            {{ currentUser ? '退出' : '登录/注册' }}
          </button>
          <button class="btn btn-primary" @click="showPublishModal = true">发布活动</button>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          class="search-input" 
          placeholder="搜索活动..."
          @keyup="searchActivities"
        />
        <select v-model="selectedCategory" class="filter-select" @change="searchActivities">
          <option value="all">全部分类</option>
          <option value="academic">学术活动</option>
          <option value="cultural">文化活动</option>
          <option value="sports">体育活动</option>
          <option value="social">社交活动</option>
        </select>
        <button class="btn btn-primary" @click="searchActivities">搜索</button>
      </div>

      <div v-if="!showDetail">
        <h2 style="margin: 30px 0 20px; font-size: 24px;">最新活动</h2>
        <div class="activities-grid" v-if="activities.length > 0">
          <div 
            v-for="activity in activities" 
            :key="activity.id" 
            class="activity-card"
            @click="viewActivity(activity)"
          >
            <div class="activity-image">
              <img :src="activity.image" :alt="activity.title" />
            </div>
            <div class="activity-content">
              <h3>{{ activity.title }}</h3>
              <p>{{ activity.description }}</p>
              <div class="activity-info-item">
                <span>📅</span>
                <span>{{ formatDateTime(activity.time) }}</span>
              </div>
              <div class="activity-info-item">
                <span>📍</span>
                <span>{{ activity.location }}</span>
              </div>
              <div class="activity-meta">
                <span :class="['activity-category', 'category-' + activity.category]">
                  {{ getCategoryText(activity.category) }}
                </span>
                <span class="activity-publisher">{{ activity.publisher }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>没有找到活动</p>
        </div>
      </div>

      <div v-else class="activity-detail">
        <button class="btn btn-outline" @click="showDetail = false">返回列表</button>
        <div class="activity-detail-header">
          <div class="detail-image">
            <img :src="currentActivity.image" :alt="currentActivity.title" />
          </div>
          <div class="detail-header-content">
            <h2>{{ currentActivity.title }}</h2>
            <div class="detail-meta">
              <div class="detail-meta-item"><span>📅</span><span>{{ formatDateTime(currentActivity.time) }}</span></div>
              <div class="detail-meta-item"><span>📍</span><span>{{ currentActivity.location }}</span></div>
              <div class="detail-meta-item"><span>🏷️</span><span>{{ getCategoryText(currentActivity.category) }}</span></div>
              <div class="detail-meta-item"><span>👤</span><span>{{ currentActivity.publisher }}</span></div>
            </div>
          </div>
        </div>
        <div class="detail-description">{{ currentActivity.description }}</div>
        <div class="detail-actions">
          <button class="btn btn-secondary" @click="handleRegister">报名参加</button>
          <button class="btn" @click="handleFavorite">收藏</button>
          <button class="btn" @click="handleShare">分享</button>
        </div>

        <div class="comments-section">
          <h3 style="margin-bottom: 20px;">评论</h3>
          <textarea 
            class="comment-input" 
            v-model="commentContent" 
            placeholder="写下你的评论..."
          ></textarea>
          <button class="btn btn-primary" @click="addComment">发布评论</button>
          <div class="comments-list" v-if="currentActivity.comments && currentActivity.comments.length > 0">
            <div 
              v-for="comment in currentActivity.comments" 
              :key="comment.id" 
              class="comment-item"
            >
              <div class="comment-header">
                <span class="comment-author">{{ comment.author }}</span>
                <span class="comment-time">{{ formatDateTime(comment.created_at) }}</span>
              </div>
              <p>{{ comment.content }}</p>
            </div>
          </div>
          <div v-else class="empty-state">
            <p>暂无评论</p>
          </div>
        </div>
      </div>
    </div>

    <div :class="['modal-overlay', { show: showAuthModal }]" @click.self="showAuthModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>用户认证</h2>
          <span class="close" @click="showAuthModal = false">&times;</span>
        </div>
        <div class="auth-tabs">
          <div :class="['auth-tab', { active: authTab === 'login' }]" @click="authTab = 'login'">登录</div>
          <div :class="['auth-tab', { active: authTab === 'register' }]" @click="authTab = 'register'">注册</div>
        </div>
        
        <div v-if="authTab === 'login'">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="loginForm.username" />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input type="password" v-model="loginForm.password" />
          </div>
          <div class="form-actions">
            <button class="btn btn-primary" @click="handleLogin">登录</button>
          </div>
        </div>
        
        <div v-else>
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="registerForm.username" />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input type="email" v-model="registerForm.email" />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input type="password" v-model="registerForm.password" />
          </div>
          <div class="form-actions">
            <button class="btn btn-primary" @click="handleRegister">注册</button>
          </div>
        </div>
      </div>
    </div>

    <div :class="['modal-overlay', { show: showPublishModal }]" @click.self="showPublishModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>发布活动</h2>
          <span class="close" @click="showPublishModal = false">&times;</span>
        </div>
        <div class="form-group">
          <label>活动标题</label>
          <input type="text" v-model="publishForm.title" />
        </div>
        <div class="form-group">
          <label>活动描述</label>
          <textarea v-model="publishForm.description"></textarea>
        </div>
        <div class="form-group">
          <label>活动时间</label>
          <input type="datetime-local" v-model="publishForm.time" />
        </div>
        <div class="form-group">
          <label>活动地点</label>
          <input type="text" v-model="publishForm.location" />
        </div>
        <div class="form-group">
          <label>活动分类</label>
          <select v-model="publishForm.category">
            <option value="academic">学术活动</option>
            <option value="cultural">文化活动</option>
            <option value="sports">体育活动</option>
            <option value="social">社交活动</option>
          </select>
        </div>
        <div class="form-group">
          <label>发布者</label>
          <input type="text" v-model="publishForm.publisher" />
        </div>
        <div class="form-actions">
          <button class="btn" @click="showPublishModal = false">取消</button>
          <button class="btn btn-primary" @click="handlePublish">发布</button>
        </div>
      </div>
    </div>

    <div 
      v-if="notification.show" 
      :class="['notification', `notification-${notification.type}`]"
    >
      {{ notification.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const activities = ref([])
const searchQuery = ref('')
const selectedCategory = ref('all')
const showDetail = ref(false)
const currentActivity = ref(null)
const showAuthModal = ref(false)
const showPublishModal = ref(false)
const authTab = ref('login')
const commentContent = ref('')
const currentUser = ref(null)

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  email: '',
  password: ''
})

const publishForm = ref({
  title: '',
  description: '',
  time: '',
  location: '',
  category: 'academic',
  publisher: ''
})

const notification = ref({
  show: false,
  message: '',
  type: 'success'
})

const categories = {
  academic: '学术活动',
  cultural: '文化活动',
  sports: '体育活动',
  social: '社交活动'
}

function showNotification(message, type = 'success') {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

function formatDateTime(dateTimeString) {
  if (!dateTimeString) return ''
  const date = new Date(dateTimeString)
  return date.toLocaleString('zh-CN')
}

function getCategoryText(category) {
  return categories[category] || category
}

async function fetchActivities() {
  try {
    const response = await axios.get('/api/activities/')
    activities.value = response.data
  } catch (error) {
    console.error('Failed to fetch activities:', error)
    showNotification('获取活动列表失败', 'error')
  }
}

async function searchActivities() {
  try {
    const params = new URLSearchParams()
    if (searchQuery.value) params.append('search', searchQuery.value)
    if (selectedCategory.value !== 'all') params.append('category', selectedCategory.value)
    
    const response = await axios.get('/api/activities/', { params })
    activities.value = response.data
  } catch (error) {
    console.error('Failed to search activities:', error)
    showNotification('搜索失败', 'error')
  }
}

function viewActivity(activity) {
  currentActivity.value = activity
  showDetail.value = true
}

async function handleLogin() {
  try {
    const response = await axios.post('/api/login/', loginForm.value)
    if (response.data.status === 'success') {
      currentUser.value = response.data
      showAuthModal.value = false
      loginForm.value = { username: '', password: '' }
      showNotification('登录成功')
    }
  } catch (error) {
    showNotification(error.response?.data?.message || '登录失败', 'error')
  }
}

async function handleRegister() {
  try {
    const response = await axios.post('/api/register/', registerForm.value)
    if (response.data.status === 'success') {
      currentUser.value = response.data
      showAuthModal.value = false
      registerForm.value = { username: '', email: '', password: '' }
      showNotification('注册成功')
    }
  } catch (error) {
    showNotification(error.response?.data?.message || '注册失败', 'error')
  }
}

function logout() {
  currentUser.value = null
  showNotification('已退出登录')
}

async function handlePublish() {
  if (!currentUser.value) {
    showNotification('请先登录', 'error')
    showAuthModal.value = true
    return
  }

  if (!publishForm.value.title || !publishForm.value.description || !publishForm.value.time || !publishForm.value.location || !publishForm.value.publisher) {
    showNotification('请填写所有字段', 'error')
    return
  }

  try {
    const activityData = {
      ...publishForm.value,
      image: `https://picsum.photos/400/225?random=${Date.now()}`
    }
    
    await axios.post('/api/activities/', activityData)
    showPublishModal.value = false
    publishForm.value = {
      title: '',
      description: '',
      time: '',
      location: '',
      category: 'academic',
      publisher: ''
    }
    await fetchActivities()
    showNotification('活动发布成功')
  } catch (error) {
    showNotification('发布失败', 'error')
  }
}

async function handleRegisterActivity() {
  if (!currentUser.value) {
    showNotification('请先登录', 'error')
    showAuthModal.value = true
    return
  }

  try {
    await axios.post(`/api/activities/${currentActivity.value.id}/register/`, {
      user_id: currentUser.value.id
    })
    showNotification('报名成功')
  } catch (error) {
    showNotification(error.response?.data?.message || '报名失败', 'error')
  }
}

async function handleFavorite() {
  if (!currentUser.value) {
    showNotification('请先登录', 'error')
    showAuthModal.value = true
    return
  }

  try {
    await axios.post(`/api/activities/${currentActivity.value.id}/favorites/`, {
      user_id: currentUser.value.id
    })
    showNotification('收藏成功')
  } catch (error) {
    showNotification(error.response?.data?.message || '收藏失败', 'error')
  }
}

function handleShare() {
  navigator.clipboard.writeText(window.location.href).then(() => {
    showNotification('链接已复制')
  })
}

async function addComment() {
  if (!currentUser.value) {
    showNotification('请先登录', 'error')
    showAuthModal.value = true
    return
  }

  if (!commentContent.value.trim()) {
    showNotification('请输入评论内容', 'error')
    return
  }

  try {
    await axios.post(`/api/activities/${currentActivity.value.id}/comments/`, {
      author: currentUser.value.username,
      content: commentContent.value
    })
    commentContent.value = ''
    await fetchActivityDetail(currentActivity.value.id)
    showNotification('评论发布成功')
  } catch (error) {
    showNotification('评论发布失败', 'error')
  }
}

async function fetchActivityDetail(id) {
  try {
    const response = await axios.get(`/api/activities/${id}/`)
    currentActivity.value = response.data
  } catch (error) {
    console.error('Failed to fetch activity detail:', error)
  }
}

onMounted(() => {
  fetchActivities()
})
</script>
