<template>
  <div class="min-h-dvh flex" style="background: linear-gradient(135deg, #FFF8F5 0%, #FFE4EC 50%, #EDE8FF 100%)">

    <!-- Sidebar -->
    <aside class="w-60 bg-white/80 backdrop-blur-md border-r border-white/60 shadow-sm flex flex-col fixed h-full z-40">
      <!-- Brand -->
      <div class="px-5 py-4 border-b border-pink-pale/50">
        <router-link to="/admin" class="flex items-center gap-2">
          <span class="text-xl">💝</span>
          <span class="text-lg font-black text-gradient">TryDate</span>
        </router-link>
        <p class="text-[11px] text-text-sub mt-0.5 ml-8">管理后台</p>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 space-y-1">
        <router-link v-for="item in navItems" :key="item.to" :to="item.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
          :class="isActive(item.to) ? 'bg-pink-pale shadow-sm' : 'hover:bg-pink-pale/40'">
          <span class="text-lg">{{ item.icon }}</span>
          <span class="text-sm font-bold"
            :class="isActive(item.to) ? 'text-pink-heart' : 'text-text-sub group-hover:text-text-main'">
            {{ item.label }}
          </span>
        </router-link>
      </nav>

      <!-- User info -->
      <div class="px-4 py-3 border-t border-pink-pale/50">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-gradient-heart flex items-center justify-center text-white text-sm font-bold">
            {{ auth.user?.nickname?.[0] || 'A' }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-bold text-text-main truncate">{{ auth.user?.nickname }}</p>
            <p class="text-[10px] text-mint font-semibold">管理员</p>
          </div>
          <button @click="handleLogout" class="text-text-sub hover:text-pink-heart transition-colors" title="退出">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 ml-60">
      <!-- Top bar -->
      <header class="sticky top-0 z-30 bg-white/70 backdrop-blur-md border-b border-white/60 px-6 py-3 flex items-center justify-between">
        <h1 class="text-lg font-black text-text-main">{{ currentPageTitle }}</h1>
        <div class="flex items-center gap-3">
          <span class="text-xs text-text-sub">{{ currentTime }}</span>
          <router-link to="/app/match" class="text-xs font-bold text-pink-heart bg-pink-pale px-3 py-1.5 rounded-xl hover:shadow-sm transition-shadow">
            返回前台
          </router-link>
        </div>
      </header>

      <!-- Page content -->
      <div class="p-6">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const navItems = [
  { to: '/admin/dashboard', icon: ' ', label: '仪表盘' },
  { to: '/admin/users', icon: ' ', label: '用户管理' },
  { to: '/admin/matches', icon: ' ', label: '匹配记录' },
  { to: '/admin/posts', icon: ' ', label: '动态管理' },
  { to: '/admin/reports', icon: ' ', label: '举报管理' },
]

const pageTitles: Record<string, string> = {
  '/admin/dashboard': '仪表盘',
  '/admin/users': '用户管理',
  '/admin/matches': '匹配记录',
  '/admin/posts': '动态管理',
  '/admin/reports': '举报管理',
}

const currentPageTitle = computed(() => pageTitles[route.path] || '管理后台')

function isActive(to: string) {
  return route.path === to || route.path.startsWith(to + '/')
}

const currentTime = ref(dayjs().format('YYYY-MM-DD HH:mm'))
let timer: ReturnType<typeof setInterval>
onMounted(() => { timer = setInterval(() => { currentTime.value = dayjs().format('YYYY-MM-DD HH:mm') }, 1000) })
onUnmounted(() => clearInterval(timer))

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.page-enter-active, .page-leave-active { transition: all 0.2s ease; }
.page-enter-from { opacity: 0; transform: translateY(8px); }
.page-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
