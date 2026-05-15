<template>
  <div>
    <!-- Toolbar -->
    <div class="card mb-4 flex items-center gap-3">
      <input v-model="search" @input="debouncedFetch" placeholder="搜索昵称、邮箱、手机号"
        class="input-field flex-1 !py-2 !text-sm" />
      <select v-model="statusFilter" @change="fetchUsers" class="input-field !w-32 !py-2 !text-sm">
        <option value="">全部状态</option>
        <option value="active">正常</option>
        <option value="banned">封禁</option>
      </select>
    </div>

    <!-- Table -->
    <div class="card overflow-hidden p-0">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-pink-pale/50">
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">用户</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">邮箱</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">性别</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">状态</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">问卷</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">注册时间</th>
            <th class="text-right px-4 py-3 font-bold text-text-sub text-xs">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id"
            class="border-b border-pink-pale/30 hover:bg-pink-pale/20 transition-colors">
            <td class="px-4 py-3">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-full bg-gradient-heart flex items-center justify-center text-white text-xs font-bold">
                  {{ user.nickname[0] }}
                </div>
                <span class="font-semibold text-text-main">{{ user.nickname }}</span>
                <span v-if="user.is_staff" class="text-[10px] bg-lilac-pale text-lilac-deep px-1.5 py-0.5 rounded-full font-bold">管理员</span>
              </div>
            </td>
            <td class="px-4 py-3 text-text-sub">{{ user.email || '-' }}</td>
            <td class="px-4 py-3">{{ user.gender === 'male' ? '男' : user.gender === 'female' ? '女' : '其他' }}</td>
            <td class="px-4 py-3">
              <span class="text-xs font-bold px-2 py-1 rounded-full"
                :class="user.status === 'active' ? 'bg-mint/20 text-mint' : 'bg-red-100 text-red-500'">
                {{ user.status === 'active' ? '正常' : '封禁' }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center gap-2">
                <div class="w-16 h-1.5 bg-lilac-pale rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all"
                    :class="user.questionnaire_completion >= 70 ? 'bg-mint' : 'bg-amber'"
                    :style="{ width: user.questionnaire_completion + '%' }" />
                </div>
                <span class="text-xs text-text-sub">{{ user.questionnaire_completion }}%</span>
              </div>
            </td>
            <td class="px-4 py-3 text-text-sub text-xs">{{ formatDate(user.created_at) }}</td>
            <td class="px-4 py-3 text-right space-x-2">
              <button v-if="user.status === 'active' && !user.is_staff"
                @click="resetMatch(user)" class="text-xs font-bold text-amber hover:text-amber/80 transition-colors">
                重置匹配
              </button>
              <button v-if="user.status === 'active' && !user.is_staff"
                @click="banUser(user)" class="text-xs font-bold text-red-500 hover:text-red-600 transition-colors">
                封禁
              </button>
              <button v-else-if="user.status === 'banned'"
                @click="unbanUser(user)" class="text-xs font-bold text-mint hover:text-mint/80 transition-colors">
                解封
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="users.length === 0 && !loading" class="py-12 text-center text-text-sub">
        暂无用户数据
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-4">
      <button v-for="p in totalPages" :key="p" @click="page = p; fetchUsers()"
        class="w-8 h-8 rounded-lg text-sm font-bold transition-all"
        :class="p === page ? 'bg-gradient-heart text-white shadow-sm' : 'bg-white text-text-sub hover:bg-pink-pale'">
        {{ p }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/api'
import { toast } from 'vue3-toastify'
import dayjs from 'dayjs'

const users = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const search = ref('')
const statusFilter = ref('')
const loading = ref(true)
const pageSize = 20
const totalPages = computed(() => Math.ceil(total.value / pageSize))

let debounceTimer: ReturnType<typeof setTimeout>
function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; fetchUsers() }, 300)
}

async function fetchUsers() {
  loading.value = true
  try {
    const params: Record<string, string> = { page: String(page.value) }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    const res = await adminApi.users(params)
    users.value = res.data.results
    total.value = res.data.total
  } catch {} finally { loading.value = false }
}

async function banUser(user: any) {
  await adminApi.banUser(user.id)
  toast.success(`已封禁 ${user.nickname}`)
  fetchUsers()
}

async function unbanUser(user: any) {
  await adminApi.unbanUser(user.id)
  toast.success(`已解封 ${user.nickname}`)
  fetchUsers()
}

async function resetMatch(user: any) {
  await adminApi.resetMatchCount(user.id)
  toast.success(`已重置 ${user.nickname} 的匹配次数`)
}

function formatDate(d: string) { return dayjs(d).format('YYYY-MM-DD') }

onMounted(fetchUsers)
</script>
