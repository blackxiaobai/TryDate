<template>
  <div>
    <!-- Toolbar -->
    <div class="card mb-4 flex items-center gap-3">
      <h3 class="text-sm font-bold text-text-main">共 {{ total }} 条匹配记录</h3>
      <div class="flex-1" />
      <select v-model="statusFilter" @change="page = 1; fetchMatches()" class="input-field !w-36 !py-2 !text-sm">
        <option value="">全部状态</option>
        <option value="pending">等待确认</option>
        <option value="matched">双向心动</option>
        <option value="missed">已错过</option>
      </select>
    </div>

    <!-- Table -->
    <div class="card overflow-hidden p-0">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-pink-pale/50">
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">周次</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">用户A</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">用户B</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">契合度</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">状态</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">双方操作</th>
            <th class="text-left px-4 py-3 font-bold text-text-sub text-xs">时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in matches" :key="m.id"
            class="border-b border-pink-pale/30 hover:bg-pink-pale/20 transition-colors">
            <td class="px-4 py-3 font-semibold text-text-main">第{{ m.week_number }}周</td>
            <td class="px-4 py-3">{{ m.user_a }}</td>
            <td class="px-4 py-3">{{ m.user_b }}</td>
            <td class="px-4 py-3">
              <span class="text-xs font-bold px-2 py-1 rounded-full"
                :class="m.compatibility_score >= 80 ? 'bg-mint/20 text-mint' : m.compatibility_score >= 60 ? 'bg-amber/20 text-amber' : 'bg-lilac-pale text-text-sub'">
                {{ m.compatibility_score }}%
              </span>
            </td>
            <td class="px-4 py-3">
              <span class="text-xs font-bold px-2 py-1 rounded-full"
                :class="{
                  'bg-amber/20 text-amber': m.status === 'pending',
                  'bg-mint/20 text-mint': m.status === 'matched',
                  'bg-gray-100 text-gray-500': m.status === 'missed',
                }">
                {{ statusLabels[m.status] }}
              </span>
            </td>
            <td class="px-4 py-3 text-xs text-text-sub">
              {{ actionLabels[m.user_a_action] }} / {{ actionLabels[m.user_b_action] }}
            </td>
            <td class="px-4 py-3 text-text-sub text-xs">{{ formatDate(m.matched_at) }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="matches.length === 0" class="py-12 text-center text-text-sub">暂无匹配记录</div>
    </div>

    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-4">
      <button v-for="p in totalPages" :key="p" @click="page = p; fetchMatches()"
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
import dayjs from 'dayjs'

const matches = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const statusFilter = ref('')
const pageSize = 20
const totalPages = computed(() => Math.ceil(total.value / pageSize))

const statusLabels: Record<string, string> = { pending: '等待确认', matched: '双向心动', missed: '已错过' }
const actionLabels: Record<string, string> = { pending: '待操作', liked: '心动', passed: '再想想' }

async function fetchMatches() {
  const params: Record<string, string> = { page: String(page.value) }
  if (statusFilter.value) params.status = statusFilter.value
  const res = await adminApi.matches(params)
  matches.value = res.data.results
  total.value = res.data.total
}

function formatDate(d: string) { return dayjs(d).format('MM-DD HH:mm') }

onMounted(fetchMatches)
</script>
