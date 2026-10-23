<script setup>
import { onMounted, ref } from 'vue'

const tasks = ref([])
const loading = ref(false)
const errorMessage = ref('')

async function loadTasks() {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('/api/tasks')

    if (!response.ok) {
      throw new Error('请求失败，状态码：' + response.status)
    }

    tasks.value = await response.json()
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}

onMounted(loadTasks)
</script>

<template>
  <main class="page">
    <h1>Mini-Jira 任务列表</h1>

    <button @click="loadTasks" :disabled="loading">
      刷新任务
    </button>

    <p v-if="loading">正在加载任务……</p>

    <p v-else-if="errorMessage" role="alert">
      {{ errorMessage }}
    </p>

    <p v-else-if="tasks.length === 0">暂无任务</p>

    <ul v-else>
      <li v-for="task in tasks" :key="task.id">
        <strong>{{ task.title }}</strong>
        <span> — {{ task.status }}</span>
        <p>{{ task.description }}</p>
      </li>
    </ul>
  </main>
</template>

<style scoped>
.page {
  padding: 24px;
  text-align: left;
}

h1 {
  font-size: 28px;
}

li {
  margin: 16px 0;
}
</style>