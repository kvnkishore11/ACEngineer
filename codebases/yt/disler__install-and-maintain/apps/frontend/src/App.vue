<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Task {
  id: number
  title: string
  description: string | null
  completed: boolean
  created_at: string
}

const API_URL = 'http://localhost:8000'

const tasks = ref<Task[]>([])
const newTitle = ref('')
const newDescription = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchTasks() {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`${API_URL}/tasks`)
    if (!res.ok) throw new Error('Failed to fetch tasks')
    tasks.value = await res.json()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
  } finally {
    loading.value = false
  }
}

async function createTask() {
  if (!newTitle.value.trim()) return
  try {
    const res = await fetch(`${API_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: newTitle.value,
        description: newDescription.value || null
      })
    })
    if (!res.ok) throw new Error('Failed to create task')
    newTitle.value = ''
    newDescription.value = ''
    await fetchTasks()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
  }
}

async function toggleTask(task: Task) {
  try {
    const res = await fetch(`${API_URL}/tasks/${task.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !task.completed })
    })
    if (!res.ok) throw new Error('Failed to update task')
    await fetchTasks()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
  }
}

async function deleteTask(id: number) {
  try {
    const res = await fetch(`${API_URL}/tasks/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Failed to delete task')
    await fetchTasks()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
  }
}

onMounted(fetchTasks)
</script>

<template>
  <div class="container">
    <h1>Task Manager</h1>
    <p class="subtitle">Claude Code Setup Hook Demo</p>

    <div v-if="error" class="error">{{ error }}</div>

    <form @submit.prevent="createTask" class="form">
      <input
        v-model="newTitle"
        type="text"
        placeholder="Task title"
        required
      />
      <input
        v-model="newDescription"
        type="text"
        placeholder="Description (optional)"
      />
      <button type="submit">Add Task</button>
    </form>

    <div v-if="loading" class="loading">Loading...</div>

    <ul v-else class="task-list">
      <li v-for="task in tasks" :key="task.id" :class="{ completed: task.completed }">
        <div class="task-content">
          <input
            type="checkbox"
            :checked="task.completed"
            @change="toggleTask(task)"
          />
          <div class="task-info">
            <span class="title">{{ task.title }}</span>
            <span v-if="task.description" class="description">{{ task.description }}</span>
          </div>
        </div>
        <button class="delete" @click="deleteTask(task.id)">Delete</button>
      </li>
    </ul>

    <p v-if="!loading && tasks.length === 0" class="empty">No tasks yet. Add one above!</p>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin-bottom: 0.25rem;
}

.subtitle {
  color: #888;
  margin-bottom: 2rem;
}

.error {
  background: #fee;
  color: #c00;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.form input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form button {
  padding: 0.5rem 1rem;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.form button:hover {
  background: #3aa876;
}

.loading {
  text-align: center;
  color: #888;
}

.task-list {
  list-style: none;
  padding: 0;
}

.task-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.task-list li.completed {
  background: #f9f9f9;
}

.task-list li.completed .title {
  text-decoration: line-through;
  color: #888;
}

.task-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.task-info {
  display: flex;
  flex-direction: column;
}

.title {
  font-weight: 500;
}

.description {
  font-size: 0.85rem;
  color: #666;
}

.delete {
  padding: 0.25rem 0.5rem;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.delete:hover {
  background: #ee5a5a;
}

.empty {
  text-align: center;
  color: #888;
}
</style>
