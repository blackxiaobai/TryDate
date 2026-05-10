<template>
  <div>
    <!-- Stats cards -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div v-for="stat in stats" :key="stat.label"
        class="card hover:shadow-card-hover transition-shadow duration-200 cursor-default">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg" :class="stat.bg">
            {{ stat.icon }}
          </div>
          <div>
            <p class="text-2xl font-black text-text-main">{{ stat.value }}</p>
            <p class="text-xs text-text-sub">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="card mb-6">
      <h3 class="text-sm font-bold text-text-main mb-4">快捷操作</h3>
      <div class="flex gap-3">
        <router-link to="/admin/users" class="btn-outline text-sm py-2 px-4">
           用户管理
        </router-link>
        <router-link to="/admin/posts" class="btn-outline text-sm py-2 px-4">
           动态管理
        </router-link>
        <router-link to="/admin/reports" class="btn-outline text-sm py-2 px-4">
          ️ 举报管理
        </router-link>
      </div>
    </div>

    <!-- Recent stats summary -->
    <div class="grid grid-cols-2 gap-4">
      <div class="card">
        <h3 class="text-sm font-bold text-text-main mb-3">用户概况</h3>
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-text-sub">总用户数</span>
            <span class="text-lg font-bold text-text-main">{{ data.total_users || 0 }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-text-sub">活跃用户</span>
            <span class="text-lg font-bold text-mint">{{ data.active_users || 0 }}</span>
          </div>
          <div class="h-2 bg-lilac-pale rounded-full overflow-hidden">
            <div class="h-full bg-gradient-heart rounded-full transition-all duration-500"
              :style="{ width: data.total_users ? (data.active_users / data.total_users * 100) + '%' : '0%' }" />
          </div>
        </div>
      </div>

      <div class="card">
        <h3 class="text-sm font-bold text-text-main mb-3">平台数据</h3>
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-text-sub">总消息数</span>
            <span class="text-lg font-bold text-lilac-deep">{{ data.total_messages || 0 }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-text-sub">成功匹配</span>
            <span class="text-lg font-bold text-pink-heart">{{ data.matched_pairs || 0 }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-text-sub">待处理举报</span>
            <span class="text-lg font-bold" :class="data.pending_reports ? 'text-amber' : 'text-mint'">
              {{ data.pending_reports || 0 }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'

const data = ref<any>({})
const loading = ref(true)

const stats = [
  { icon: ' ', label: '总用户', value: 0, bg: 'bg-pink-pale', key: 'total_users' },
  { icon: ' ', label: '本周匹配', value: 0, bg: 'bg-lilac-pale', key: 'weekly_matches' },
  { icon: ' ', label: '总消息', value: 0, bg: 'bg-mint/20', key: 'total_messages' },
  { icon: '⚠️', label: '待处理举报', value: 0, bg: 'bg-amber/20', key: 'pending_reports' },
]

onMounted(async () => {
  try {
    const res = await adminApi.dashboard()
    data.value = res.data
    stats.forEach(s => s.value = res.data[s.key] || 0)
  } catch {} finally { loading.value = false }
})
</script>
