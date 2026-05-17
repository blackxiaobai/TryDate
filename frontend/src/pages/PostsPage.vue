<template>
  <div class="page-container pt-8 px-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-5">
      <h1 class="text-2xl font-black text-text-main">话题动态 🌸</h1>
      <button @click="showCompose = true"
        class="w-10 h-10 rounded-xl bg-gradient-heart flex items-center justify-center shadow-card active:scale-95 transition-transform">
        <PlusIcon class="w-5 h-5 text-white" />
      </button>
    </div>

    <!-- Posts list -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="card space-y-2 animate-pulse">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-lilac-pale"></div>
          <div class="h-3 bg-lilac-pale rounded-xl w-20"></div>
        </div>
        <div class="h-4 bg-lilac-pale rounded-xl"></div>
        <div class="h-4 bg-lilac-pale rounded-xl w-3/4"></div>
      </div>
    </div>

    <div v-else-if="posts.length === 0" class="flex flex-col items-center justify-center min-h-[50vh] gap-4 text-center">
      <div class="w-20 h-20 rounded-full bg-gradient-soft flex items-center justify-center text-3xl shadow-card animate-float">📭</div>
      <p class="text-text-sub text-sm">还没有动态，来发第一条吧！</p>
      <button @click="showCompose=true" class="btn-primary px-6 py-3">发布动态 🌸</button>
    </div>

    <div v-else class="space-y-3 pb-4">
      <transition-group name="list">
        <div v-for="post in posts" :key="post.id" class="card">
          <!-- Author row -->
          <div class="flex items-center gap-2.5 mb-3">
            <div class="w-9 h-9 rounded-full bg-gradient-soft flex items-center justify-center text-sm shadow-sm">
              {{ post.is_anonymous ? '🎭' : '🌸' }}
            </div>
            <div>
              <p class="text-sm font-bold text-text-main">{{ post.author_display }}</p>
              <p class="text-[11px] text-text-sub">{{ formatTime(post.created_at) }}</p>
            </div>
            <div v-if="post.is_anonymous" class="ml-auto">
              <span class="text-[10px] bg-lilac-pale text-lilac-deep px-2 py-0.5 rounded-full font-semibold">匿名</span>
            </div>
            <button v-if="post.is_owner" @click="deletePost(post)"
              class="ml-auto text-text-sub/60 active:scale-90 transition-transform">
              <Trash2Icon class="w-4 h-4" />
            </button>
            <button v-if="!post.is_owner" @click="openReportPost(post)" class="ml-auto text-text-sub active:scale-90 transition-transform">
              <FlagIcon class="w-4 h-4" />
            </button>
          </div>

          <!-- Content -->
          <p class="text-sm text-text-main leading-relaxed mb-3 font-medium">{{ post.content }}</p>

          <!-- Actions -->
          <div class="flex items-center gap-4 pt-2 border-t border-lilac-pale/50">
            <button @click="toggleLike(post)"
              class="flex items-center gap-1.5 transition-transform active:scale-110"
              :class="post.is_liked ? 'text-pink-heart' : 'text-text-sub'">
              <HeartIcon class="w-4 h-4" :class="post.is_liked ? 'fill-pink-heart' : ''" />
              <span class="text-xs font-bold">{{ post.like_count }}</span>
            </button>
            <button @click="toggleComments(post)"
              class="flex items-center gap-1.5 text-text-sub transition-transform active:scale-110">
              <MessageCircleIcon class="w-4 h-4" />
              <span class="text-xs font-bold">{{ post.comment_count }}</span>
            </button>
          </div>

          <!-- Comments section -->
          <div v-if="post._showComments" class="mt-3 space-y-2 animate-slide-up">
            <div v-if="post._loadingComments" class="text-center py-2">
              <span class="text-xs text-text-sub">加载评论中…</span>
            </div>
            <template v-else>
              <div v-for="c in post._comments" :key="c.id" class="flex items-start gap-2 bg-cream/50 rounded-xl px-3 py-2">
                <span class="text-xs mt-0.5">{{ c.is_anonymous ? '🎭' : '🌸' }}</span>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-bold text-text-main">{{ c.author_display }}</span>
                    <span class="text-[10px] text-text-sub">{{ formatTime(c.created_at) }}</span>
                    <button @click="openReportComment(post, c)" class="ml-auto text-text-sub/50 active:scale-90">
                      <FlagIcon class="w-3 h-3" />
                    </button>
                  </div>
                  <p class="text-xs text-text-main mt-0.5">{{ c.content }}</p>
                </div>
              </div>
              <div v-if="post._comments?.length === 0" class="text-center py-1">
                <span class="text-[11px] text-text-sub">暂无评论，来说两句吧～</span>
              </div>
              <!-- Comment input -->
              <div class="flex items-center gap-2 mt-1">
                <EmojiPicker @select="(e) => post._newComment = (post._newComment || '') + e" />
                <input v-model="post._newComment" placeholder="写评论…" maxlength="100"
                  class="flex-1 px-3 py-1.5 rounded-xl bg-cream text-xs text-text-main placeholder-text-sub outline-none focus:ring-1 focus:ring-lilac" />
                <button @click="post._newAnonymous = !post._newAnonymous"
                  class="text-[10px] px-2 py-1 rounded-lg transition-colors"
                  :class="post._newAnonymous ? 'bg-lilac-pale text-lilac-deep' : 'bg-cream text-text-sub'">
                  {{ post._newAnonymous ? '匿名' : '公开' }}
                </button>
                <button @click="submitComment(post)" :disabled="!post._newComment?.trim()"
                  class="text-xs font-bold text-pink-heart disabled:opacity-30">发送</button>
              </div>
            </template>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Compose sheet -->
    <div v-if="showCompose" @click.self="showCompose=false"
      class="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-end">
      <div class="w-full bg-white rounded-t-3xl p-5 animate-slide-up shadow-2xl">
        <div class="w-10 h-1 bg-gray-200 rounded-full mx-auto mb-5"></div>
        <h3 class="text-lg font-black text-text-main mb-4">发布动态 🌸</h3>

        <textarea v-model="newContent" placeholder="说说你的校园故事…（最多200字）"
          maxlength="200" rows="4"
          class="input-field resize-none mb-3 text-sm" />

        <div class="mb-3">
          <EmojiPicker @select="(e) => newContent += e" />
        </div>

        <div class="flex items-center justify-between mb-4">
          <label class="flex items-center gap-2 cursor-pointer">
            <div @click="isAnonymous=!isAnonymous"
              class="w-10 h-6 rounded-full transition-colors duration-200 relative"
              :class="isAnonymous ? 'bg-gradient-heart' : 'bg-gray-200'">
              <div class="w-4 h-4 bg-white rounded-full absolute top-1 transition-transform duration-200 shadow"
                :class="isAnonymous ? 'translate-x-5' : 'translate-x-1'"></div>
            </div>
            <span class="text-sm font-semibold text-text-sub">匿名发布</span>
          </label>
          <span class="text-xs text-text-sub">{{ newContent.length }}/200</span>
        </div>

        <button @click="publishPost" :disabled="!newContent.trim() || publishing"
          class="btn-primary w-full py-3.5 disabled:opacity-40">
          {{ publishing ? '发布中…' : '发布 🌸' }}
        </button>
      </div>
    </div>

    <!-- Report dialog -->
    <div v-if="showReport" @click.self="showReport=false"
      class="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm flex items-end">
      <div class="w-full bg-white rounded-t-3xl p-5 space-y-3 animate-slide-up">
        <div class="w-10 h-1 bg-gray-200 rounded-full mx-auto mb-2"></div>
        <h3 class="font-black text-text-main text-sm">举报原因</h3>
        <div class="flex flex-wrap gap-2">
          <button v-for="(label, key) in reportReasons" :key="key"
            @click="reportReason = key"
            class="px-4 py-2 rounded-xl text-xs font-bold transition-all"
            :class="reportReason === key ? 'bg-amber/20 text-amber ring-2 ring-amber/30' : 'bg-gray-100 text-text-sub'">
            {{ label }}
          </button>
        </div>
        <textarea v-model="reportDesc" placeholder="补充说明（可选）" rows="2"
          class="w-full px-4 py-2.5 rounded-2xl bg-cream border-2 border-transparent text-sm text-text-main placeholder-text-sub outline-none focus:border-amber/40 resize-none" />
        <button @click="submitReport" :disabled="!reportReason || reporting"
          class="w-full py-3 rounded-2xl bg-gradient-heart text-white font-bold text-sm disabled:opacity-40">
          {{ reporting ? '提交中…' : '提交举报' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { PlusIcon, HeartIcon, MessageCircleIcon, FlagIcon, Trash2Icon } from 'lucide-vue-next'
import { toast } from 'vue3-toastify'
import { postsApi, chatApi } from '@/api'
import EmojiPicker from '@/components/EmojiPicker.vue'
import dayjs from 'dayjs'

const loading = ref(true)
const posts = ref<any[]>([])
const showCompose = ref(false)
const newContent = ref('')
const isAnonymous = ref(false)
const publishing = ref(false)

// Report state
const showReport = ref(false)
const reportReason = ref('')
const reportDesc = ref('')
const reporting = ref(false)
const reportTarget = ref<{ type: 'post' | 'comment', postId?: number, commentId?: number }>({ type: 'post' })
const reportReasons: Record<string, string> = {
  harassment: '骚扰/辱骂',
  inappropriate_content: '不当内容',
  fake: '虚假信息',
  other: '其他',
}

function formatTime(t: string) {
  const d = dayjs(t)
  if (dayjs().isSame(d, 'day')) return '今天 ' + d.format('HH:mm')
  return d.format('M月D日')
}

async function toggleLike(post: any) {
  try {
    const res = await postsApi.like(post.id)
    post.is_liked = res.data.liked
    post.like_count = res.data.like_count
  } catch {}
}

async function publishPost() {
  if (!newContent.value.trim()) return
  publishing.value = true
  try {
    const res = await postsApi.create({ content: newContent.value.trim(), is_anonymous: isAnonymous.value })
    posts.value.unshift({ ...res.data, _showComments: false, _comments: [], _newComment: '', _newAnonymous: false, _loadingComments: false })
    newContent.value = ''
    showCompose.value = false
    toast.success('发布成功 🌸')
  } catch {} finally { publishing.value = false }
}

async function toggleComments(post: any) {
  if (post._showComments) {
    post._showComments = false
    return
  }
  post._showComments = true
  if (!post._comments) {
    post._loadingComments = true
    post._comments = []
    try {
      const res = await postsApi.comments(post.id)
      post._comments = res.data
    } catch {} finally { post._loadingComments = false }
  }
}

async function submitComment(post: any) {
  const content = post._newComment?.trim()
  if (!content) return
  try {
    const res = await postsApi.comment(post.id, { content, is_anonymous: post._newAnonymous || false })
    post._comments.push(res.data)
    post.comment_count = (post.comment_count || 0) + 1
    post._newComment = ''
  } catch { toast.error('评论失败') }
}

async function deletePost(post: any) {
  if (!confirm('确定要删除这条动态吗？')) return
  try {
    await postsApi.delete(post.id)
    posts.value = posts.value.filter((p: any) => p.id !== post.id)
    toast.success('已删除')
  } catch { toast.error('删除失败') }
}

function openReportPost(post: any) {
  reportTarget.value = { type: 'post', postId: post.id }
  reportReason.value = ''
  reportDesc.value = ''
  showReport.value = true
}

function openReportComment(post: any, comment: any) {
  reportTarget.value = { type: 'comment', postId: post.id, commentId: comment.id }
  reportReason.value = ''
  reportDesc.value = ''
  showReport.value = true
}

async function submitReport() {
  if (!reportReason.value || reporting.value) return
  reporting.value = true
  try {
    const data: any = { reason: reportReason.value, description: reportDesc.value || undefined }
    if (reportTarget.value.type === 'post') {
      data.target_post = reportTarget.value.postId
    } else {
      data.target_comment = reportTarget.value.commentId
    }
    await chatApi.report(data)
    toast.success('举报已提交，我们会尽快处理')
    showReport.value = false
  } catch { toast.error('举报失败') } finally { reporting.value = false }
}

onMounted(async () => {
  try {
    const res = await postsApi.list()
    posts.value = (res.data.results || res.data).map((p: any) => ({
      ...p,
      _showComments: false,
      _comments: null,
      _newComment: '',
      _newAnonymous: false,
      _loadingComments: false,
    }))
  } catch {} finally { loading.value = false }
})
</script>

<style scoped>
.list-enter-active { animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.list-leave-active { animation: fadeOut 0.2s ease; }
@keyframes fadeOut { to { opacity: 0; transform: scale(0.95); } }
</style>
