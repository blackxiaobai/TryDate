<template>
  <div class="min-h-dvh flex flex-col" style="background:linear-gradient(160deg,#FFF8F5 0%,#FFE4EC 50%,#EDE8FF 100%)">

    <!-- Back + logo -->
    <header class="px-6 pt-10 pb-2 flex items-center gap-3">
      <router-link to="/" class="w-9 h-9 rounded-xl bg-white/70 flex items-center justify-center shadow-sm">
        <ArrowLeftIcon class="w-5 h-5 text-text-main" />
      </router-link>
      <span class="text-lg font-black text-gradient">TryDate</span>
    </header>

    <div class="flex-1 flex flex-col justify-center px-6 pb-10">

      <!-- Title -->
      <div class="text-center mb-8 animate-slide-up">
        <div class="text-5xl mb-3">{{ isRegister ? '🌸' : '💝' }}</div>
        <h2 class="text-2xl font-black text-text-main">{{ isRegister ? '加入心动社区' : '欢迎回来' }}</h2>
        <p class="text-text-sub text-sm mt-1">{{ isRegister ? '开启你的恋爱新旅程' : '继续寻找那个刚刚好的人' }}</p>
      </div>

      <!-- Card -->
      <div class="card max-w-sm mx-auto w-full animate-slide-up" style="animation-delay:0.1s">

        <!-- Tab toggle -->
        <div class="flex bg-lilac-pale rounded-2xl p-1 mb-6">
          <button @click="isRegister=false"
            class="flex-1 py-2 rounded-xl text-sm font-bold transition-all duration-200"
            :class="!isRegister ? 'bg-gradient-heart text-white shadow-sm' : 'text-text-sub'">
            登录
          </button>
          <button @click="isRegister=true"
            class="flex-1 py-2 rounded-xl text-sm font-bold transition-all duration-200"
            :class="isRegister ? 'bg-gradient-heart text-white shadow-sm' : 'text-text-sub'">
            注册
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">

          <!-- Login mode toggle (only in login) -->
          <template v-if="!isRegister">
            <div class="flex bg-cream rounded-xl p-0.5 gap-0.5">
              <button type="button" @click="loginMode='password'"
                class="flex-1 py-1.5 rounded-lg text-xs font-bold transition-all"
                :class="loginMode==='password' ? 'bg-white text-pink-heart shadow-sm' : 'text-text-sub'">
                🔑 密码登录
              </button>
              <button type="button" @click="loginMode='code'"
                class="flex-1 py-1.5 rounded-lg text-xs font-bold transition-all"
                :class="loginMode==='code' ? 'bg-white text-pink-heart shadow-sm' : 'text-text-sub'">
                📬 验证码登录
              </button>
            </div>
          </template>

          <!-- Email input -->
          <input v-model="email" type="email" placeholder="输入邮箱地址" class="input-field" required />

          <!-- Password input (register always, login password mode) -->
          <template v-if="isRegister || loginMode === 'password'">
            <input v-model="password" type="password" placeholder="输入密码（至少6位）" minlength="6" class="input-field" required />
          </template>

          <!-- Register extra fields -->
          <template v-if="isRegister">
            <input v-model="nickname" type="text" placeholder="昵称（最多10字）" maxlength="10" class="input-field" required />
            <div class="flex gap-2">
              <select v-model="gender" class="input-field flex-1">
                <option value="">性别</option>
                <option value="male">男生 🙋‍♂️</option>
                <option value="female">女生 🙋‍♀️</option>
              </select>
              <select v-model="gender_preference" class="input-field flex-1">
                <option value="">期望</option>
                <option value="male">男生</option>
                <option value="female">女生</option>
                <option value="both">不限</option>
              </select>
            </div>
          </template>

          <!-- Code row (register always, login code mode) -->
          <template v-if="isRegister || loginMode === 'code'">
            <div class="flex gap-2">
              <input v-model="code" type="text" placeholder="邮箱验证码" maxlength="6" class="input-field flex-1" required />
              <button type="button" @click="sendCode"
                :disabled="countdown > 0 || sendingCode"
                class="whitespace-nowrap px-4 py-3 rounded-2xl bg-gradient-heart text-white text-sm font-bold disabled:opacity-50 transition-all active:scale-95 shadow-sm">
                {{ countdown > 0 ? `${countdown}s` : (sendingCode ? '发送中' : '获取') }}
              </button>
            </div>
          </template>

          <button type="submit" :disabled="loading" class="btn-primary w-full py-4 text-base mt-2">
            <span v-if="loading">处理中…</span>
            <span v-else>{{ isRegister ? '立即注册 🌸' : '进入心动世界 💘' }}</span>
          </button>
        </form>
      </div>

      <p class="text-center text-xs text-text-sub mt-4 px-4">
        注册即表示同意
        <span class="text-pink-heart font-semibold">《用户协议》</span> 和
        <span class="text-pink-heart font-semibold">《隐私政策》</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from 'lucide-vue-next'
import { toast } from 'vue3-toastify'
import { userApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isRegister = ref(false)
const loginMode = ref<'password' | 'code'>('password')
const email = ref('')
const code = ref('')
const password = ref('')
const nickname = ref('')
const gender = ref('')
const gender_preference = ref('')
const loading = ref(false)
const sendingCode = ref(false)
const countdown = ref(0)

let timer: ReturnType<typeof setInterval>

async function sendCode() {
  if (!email.value) { toast.error('请先填写邮箱地址'); return }
  sendingCode.value = true
  try {
    await userApi.sendCode(email.value, 'email')
    toast.success('验证码已发送 📬')
    countdown.value = 60
    timer = setInterval(() => { if (--countdown.value <= 0) clearInterval(timer) }, 1000)
  } catch { /* handled by interceptor */ } finally { sendingCode.value = false }
}

async function handleSubmit() {
  loading.value = true
  try {
    let res
    if (isRegister.value) {
      if (!gender.value || !gender_preference.value) { toast.error('请选择性别和期望对象'); return }
      res = await userApi.register({ target: email.value, code_type: 'email', code: code.value, password: password.value, nickname: nickname.value, gender: gender.value, gender_preference: gender_preference.value })
    } else if (loginMode.value === 'password') {
      res = await userApi.loginWithPassword(email.value, password.value)
    } else {
      res = await userApi.login({ target: email.value, code_type: 'email', code: code.value })
    }
    auth.setTokens(res.data.access, res.data.refresh, res.data.user)
    toast.success(isRegister.value ? '注册成功！去完成灵魂问卷吧 ✨' : '欢迎回来 💝')
    await router.push(isRegister.value ? '/app/questionnaire' : '/app/match')
  } catch { /* handled */ } finally { loading.value = false }
}
</script>
