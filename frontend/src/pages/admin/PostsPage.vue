<template>
  <div>
    <div class="card mb-4 flex items-center gap-3">
      <h3 class="text-sm font-bold text-text-main">共 {{ total }} 条动态</h3>
      <div class="flex-1" />
      <select v-model="statusFilter" @change="page = 1; fetchPosts()" class="input-field !w-32 !py-2 !text-sm">
        <option value="">全部状态</option>
        <option value="active">正常</option>
        <option value="hidden">已隐藏</option>
      </select>
    </div>

    <div class="space-y-3">
      <div v-for="post in posts" :key="post.id" class="card hover:shadow-card-hover transition-shadow">
        <div class="flex items-start gap-3">
          <div class="w-10 h-10 rounded-full bg-gradient-heart flex items-center justify-center text-white font-bold shrink-0">
            {{ post.is_anonymous ? '?' : post.author[0] }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-bold text-text-main text-sm">{{ post.is_anonymous ? '匿名用户' : post.author }}</span>
              <span v-if="post.is_anonymous" class="text-[10px] bg-lilac-pale text-lilac-deep px-1.5 py-0.5 rounded-full">匿名</span>
              <span class="text-xs font-bold px-2 py-0.5 rounded-full"
                :class="post.status === 'active' ? 'bg-mint/20 text-mint' : 'bg-red-100 text-red-500'">
                {{ post.status === 'active' ? '正常' : '已隐藏' }}
              </span>
            </div>
            <p class="text-sm text-text-main mb-2">{{ post.content }}</p>
            <div class="flex items-center gap-4 text-xs text-text-sub">
              <span>❤️ {{ post.like_count }}</span>
              <span>{{ formatDate(post.created_at) }}</span>
            </div>
          </div>
          <div class="shrink-0 flex gap-2">
            <button v-if="post.status === 'active'" @click="hidePost(post)"
              class="text-xs font-bold text-amber hover:text-amber/80 bg-amber/10 px-3 py-1.5 rounded-xl transition-colors">
              隐藏
            </button>
            <button v-else @click="restorePost(post)"
              class="text-xs font-bold text-mint hover:text-mint/80 bg-mint/10 px-3 py-1.5 rounded-xl transition-colors">
              恢复
            </button>
          </div>
        </div>
      </div>

      <div v-if="posts.length === 0" class="card text-center py-12 text-text-sub">暂无动态</div>
    </div>

    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-4">
      <button v-for="p in totalPages" :key="p" @click="page = p; fetchPosts()"
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

const posts = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const statusFilter = ref('')
const pageSize = 20
const totalPages = computed(() => Math.ceil(total.value / pageSize))

async function fetchPosts() {
  const params: Record<string, string> = { page: String(page.value) }
  if (statusFilter.value) params.status = statusFilter.value
  const res = await adminApi.posts(params)
  posts.value = res.data.results
  total.value = res.data.total
}

async function hidePost(post: any) {
  await adminApi.hidePost(post.id)
  toast.success('已隐藏')
  fetchPosts()
}

async function restorePost(post: any) {
  await adminApi.restorePost(post.id)
  toast.success('已恢复')
  fetchPosts()
}

function formatDate(d: string) { return dayjs(d).format('MM-DD HH:mm') }

onMounted(fetchPosts)
</script>
