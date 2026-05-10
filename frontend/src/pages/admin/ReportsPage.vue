<template>
  <div>
    <div class="card mb-4 flex items-center gap-3">
      <h3 class="text-sm font-bold text-text-main">共 {{ total }} 条举报</h3>
      <div class="flex-1" />
      <select v-model="statusFilter" @change="page = 1; fetchReports()" class="input-field !w-32 !py-2 !text-sm">
        <option value="">全部状态</option>
        <option value="pending">待处理</option>
        <option value="reviewed">已审核</option>
        <option value="resolved">已处理</option>
        <option value="dismissed">已驳回</option>
      </select>
    </div>

    <div class="space-y-3">
      <div v-for="r in reports" :key="r.id" class="card hover:shadow-card-hover transition-shadow">
        <div class="flex items-start gap-3">
          <div class="w-10 h-10 rounded-xl bg-amber/10 flex items-center justify-center text-lg shrink-0">⚠️</div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-bold text-text-main text-sm">{{ r.reporter }}</span>
              <span class="text-text-sub text-xs">举报</span>
              <span class="font-bold text-text-main text-sm">{{ r.target_user }}</span>
              <span class="text-xs font-bold px-2 py-0.5 rounded-full"
                :class="{
                  'bg-amber/20 text-amber': r.status === 'pending',
                  'bg-lilac-pale text-lilac-deep': r.status === 'reviewed',
                  'bg-mint/20 text-mint': r.status === 'resolved',
                  'bg-gray-100 text-gray-500': r.status === 'dismissed',
                }">
                {{ statusLabels[r.status] }}
              </span>
            </div>
            <p class="text-xs text-text-sub mb-1">原因：{{ reasonLabels[r.reason] || r.reason }}</p>
            <p v-if="r.description" class="text-sm text-text-main">{{ r.description }}</p>
            <p class="text-xs text-text-sub mt-2">{{ formatDate(r.created_at) }}</p>
          </div>
          <div v-if="r.status === 'pending'" class="shrink-0 flex flex-col gap-1.5">
            <button @click="resolve(r, 'resolved')"
              class="text-xs font-bold text-white bg-mint px-3 py-1.5 rounded-xl hover:opacity-90 transition-opacity">
              处理
            </button>
            <button @click="resolve(r, 'dismissed')"
              class="text-xs font-bold text-text-sub bg-gray-100 px-3 py-1.5 rounded-xl hover:bg-gray-200 transition-colors">
              驳回
            </button>
          </div>
        </div>
      </div>

      <div v-if="reports.length === 0" class="card text-center py-12 text-text-sub">暂无举报</div>
    </div>

    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-4">
      <button v-for="p in totalPages" :key="p" @click="page = p; fetchReports()"
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

const reports = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const statusFilter = ref('')
const pageSize = 20
const totalPages = computed(() => Math.ceil(total.value / pageSize))

const statusLabels: Record<string, string> = { pending: '待处理', reviewed: '已审核', resolved: '已处理', dismissed: '已驳回' }
const reasonLabels: Record<string, string> = { harassment: '骚扰/辱骂', inappropriate_content: '不当内容', fake: '虚假信息', other: '其他' }

async function fetchReports() {
  const params: Record<string, string> = { page: String(page.value) }
  if (statusFilter.value) params.status = statusFilter.value
  const res = await adminApi.reports(params)
  reports.value = res.data.results
  total.value = res.data.total
}

async function resolve(r: any, action: string) {
  await adminApi.resolveReport(r.id, action)
  toast.success(action === 'resolved' ? '已处理' : '已驳回')
  fetchReports()
}

function formatDate(d: string) { return dayjs(d).format('MM-DD HH:mm') }

onMounted(fetchReports)
</script>
