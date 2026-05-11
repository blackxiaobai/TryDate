<template>
  <div class="min-h-dvh page-container" style="background:linear-gradient(160deg,#FFF8F5 0%,#FFE4EC 45%,#EDE8FF 100%)">
    <!-- Header -->
    <div class="px-5 pt-8 pb-4">
      <div class="flex items-center gap-3 mb-4">
        <router-link to="/app/match" class="w-9 h-9 rounded-xl bg-white/70 flex items-center justify-center shadow-sm">
          <ArrowLeftIcon class="w-5 h-5 text-text-main" />
        </router-link>
        <div>
          <h1 class="text-lg font-black text-text-main">灵魂测试 ✨</h1>
          <p class="text-xs text-text-sub">第 {{ currentStep + 1 }} / {{ questions.length }} 题</p>
        </div>
      </div>
      <!-- Progress bar -->
      <div class="h-2 bg-white/60 rounded-full overflow-hidden shadow-inner">
        <div class="h-full bg-gradient-heart rounded-full transition-all duration-500"
          :style="{ width: ((currentStep + 1) / questions.length * 100) + '%' }" />
      </div>
    </div>

    <!-- Question card -->
    <div class="px-5 py-2">
      <transition name="q-slide" mode="out-in">
        <div :key="currentStep" class="card animate-slide-up">

          <!-- Dimension badge -->
          <div class="inline-flex items-center gap-1.5 bg-gradient-soft px-3 py-1 rounded-full mb-4">
            <span class="text-sm">{{ questions[currentStep].emoji }}</span>
            <span class="text-xs font-bold text-pink-heart">{{ questions[currentStep].dimension }}</span>
          </div>

          <h3 class="text-lg font-black text-text-main mb-5 leading-snug">
            {{ questions[currentStep].text }}
          </h3>

          <!-- Options -->
          <div class="space-y-2.5">
            <button v-for="(opt, oi) in questions[currentStep].options" :key="oi"
              @click="questions[currentStep].multi ? toggleMulti(opt.value) : selectSingle(opt.value)"
              class="w-full text-left px-4 py-3.5 rounded-2xl border-2 font-semibold text-sm transition-all duration-200 active:scale-98"
              :class="isSelected(currentStep, opt.value)
                ? 'border-pink-heart bg-pink-pale text-pink-heart shadow-card'
                : 'border-lilac-pale bg-white/70 text-text-main hover:border-lilac'">
              <span class="mr-2">{{ opt.emoji }}</span>{{ opt.label }}
              <span v-if="questions[currentStep].multi && isSelected(currentStep, opt.value)" class="ml-1 text-xs">✓</span>
            </button>
          </div>
          <p v-if="questions[currentStep].multi" class="text-xs text-text-sub mt-3 text-center">
            可多选 · 已选 {{ multiCount(currentStep) }} 项
          </p>
        </div>
      </transition>
    </div>

    <!-- Navigation buttons -->
    <div class="fixed bottom-0 left-0 right-0 p-5 safe-bottom bg-gradient-to-t from-cream/90 to-transparent">
      <div class="max-w-sm mx-auto flex gap-3">
        <button v-if="currentStep > 0" @click="prev"
          class="btn-outline flex-1 py-3.5">
          ← 上一题
        </button>
        <button @click="next" :disabled="!answers[questions[currentStep].key] && !questions[currentStep].optional"
          class="btn-primary flex-1 py-3.5 disabled:opacity-40">
          {{ currentStep === questions.length - 1 ? '完成测试 🎉' : '下一题 →' }}
        </button>
      </div>
    </div>

    <!-- Completion overlay -->
    <div v-if="completed" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div class="card max-w-xs w-full mx-4 text-center animate-bounce-in">
        <div class="text-6xl mb-4">🎉</div>
        <h3 class="text-xl font-black text-text-main mb-2">灵魂问卷完成！</h3>
        <p class="text-text-sub text-sm mb-5">完成度 {{ completion }}%，可以参与每周心动匹配了</p>
        <button @click="goToMatch" class="btn-primary w-full py-3.5">去看本周心动 💘</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from 'lucide-vue-next'
import { toast } from 'vue3-toastify'
import { questionnaireApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const currentStep = ref(0)
const completed = ref(false)
const completion = ref(0)
const answers = reactive<Record<string, string | string[]>>({})

interface Option { value: string; emoji: string; label: string }
interface Question { key: string; dimension: string; emoji: string; text: string; options: Option[]; multi?: boolean; optional?: boolean }

const questions: Question[] = [
  // ===== 单选题（第 1-20 题）=====

  // === 性格特质 ===
  { key:'personality_type', dimension:'性格特质', emoji:'✨', text:'你更接近哪种性格？', options:[{value:'extrovert',emoji:'🎉',label:'外向，喜欢热闹'},{value:'ambivert',emoji:'🌿',label:'随心所欲，两者皆可'},{value:'introvert',emoji:'📚',label:'内向，享受独处'}] },
  { key:'mbti', dimension:'性格特质', emoji:'🔮', text:'你的 MBTI 是？', optional:true, options:[{value:'INFP',emoji:'🌙',label:'INFP'},{value:'ENFP',emoji:'🌟',label:'ENFP'},{value:'INTJ',emoji:'🔭',label:'INTJ'},{value:'ENTJ',emoji:'⚡',label:'ENTJ'},{value:'INFJ',emoji:'💫',label:'INFJ'},{value:'ENFJ',emoji:'☀️',label:'ENFJ'},{value:'ISFP',emoji:'🎨',label:'ISFP'},{value:'ESTP',emoji:'🏄',label:'ESTP'},{value:'other',emoji:'🎭',label:'其他/不清楚'}] },
  { key:'morning_mood', dimension:'性格特质', emoji:'🌄', text:'你早起后的状态是？', options:[{value:'energetic',emoji:'⚡',label:'充满活力，立刻行动'},{value:'slow',emoji:'😴',label:'需要慢慢清醒'},{value:'grumpy',emoji:'😤',label:'有点起床气'},{value:'depends',emoji:'🤷',label:'看心情'}] },

  // === 爱情观 ===
  { key:'love_priorities', dimension:'爱情观', emoji:'💕', text:'恋爱中你最看重什么？', options:[{value:'understanding',emoji:'🤝',label:'理解与陪伴'},{value:'growth',emoji:'🌱',label:'共同成长进步'},{value:'fun',emoji:'🎊',label:'快乐与浪漫'},{value:'stability',emoji:'🏠',label:'稳定与安全感'}] },
  { key:'conflict_style', dimension:'爱情观', emoji:'💬', text:'吵架了你倾向于怎么做？', options:[{value:'talk_now',emoji:'🗣️',label:'立刻沟通，不隔夜'},{value:'cool_down',emoji:'❄️',label:'先冷静，再聊'},{value:'hug_first',emoji:'🤗',label:'抱一抱，用行动说话'}] },
  { key:'space_need', dimension:'爱情观', emoji:'🌊', text:'恋爱中你需要多少私人空间？', options:[{value:'1',emoji:'🔥',label:'黏糊糊最好，24小时在一起'},{value:'2',emoji:'🌸',label:'大部分时间在一起'},{value:'3',emoji:'⚖️',label:'各自有自己的时间'},{value:'4',emoji:'🌙',label:'需要较多独处时间'}] },
  { key:'long_distance', dimension:'爱情观', emoji:'✈️', text:'你能接受异地恋吗？', options:[{value:'1',emoji:'❌',label:'完全不能'},{value:'2',emoji:'😟',label:'不太能，但短期可以'},{value:'3',emoji:'😐',label:'无所谓'},{value:'4',emoji:'💪',label:'可以，距离不是问题'}] },
  { key:'future_plan', dimension:'爱情观', emoji:'🌟', text:'毕业后你打算？', options:[{value:'local',emoji:'🏡',label:'留在本城市'},{value:'return_home',emoji:'🏘️',label:'回老家发展'},{value:'open',emoji:'🌍',label:'哪里好就去哪里'},{value:'abroad',emoji:'✈️',label:'出国深造或工作'}] },
  { key:'money_attitude', dimension:'爱情观', emoji:'💰', text:'恋爱中你对消费的态度？', options:[{value:'share',emoji:'🤝',label:'AA 或轮流请'},{value:'treat',emoji:'🎁',label:'谁收入高谁多付'},{value:'free',emoji:'💸',label:'不用太计较'},{value:'save',emoji:'🐷',label:'一起攒钱规划'}] },
  { key:'love_role', dimension:'爱情观', emoji:'🎭', text:'在恋爱中你更像？', options:[{value:'leader',emoji:'🦁',label:'主导者，喜欢安排计划'},{value:'follower',emoji:'🐰',label:'跟随者，享受被照顾'},{value:'equal',emoji:'⚖️',label:'平等伙伴，一起商量'}] },

  // === 生活习惯 ===
  { key:'sleep_schedule', dimension:'生活习惯', emoji:'🌙', text:'你是什么类型的人？', options:[{value:'early_bird',emoji:'🌅',label:'早鸟型，7点前起床'},{value:'normal',emoji:'☀️',label:'普通作息，8-10点'},{value:'night_owl',emoji:'🌙',label:'夜猫子，12点后睡'}] },
  { key:'ideal_weekend', dimension:'生活习惯', emoji:'🎡', text:'理想的周末是？', options:[{value:'outdoor',emoji:'🏕️',label:'户外探险、运动'},{value:'social',emoji:'☕',label:'逛街、咖啡、看展'},{value:'homebody',emoji:'🛋️',label:'宅家追剧、打游戏'},{value:'learning',emoji:'📖',label:'读书、学习充电'}] },
  { key:'food_style', dimension:'生活习惯', emoji:'🍜', text:'你的饮食偏好？', options:[{value:'everything',emoji:'😋',label:'什么都吃'},{value:'spicy',emoji:'🌶️',label:'无辣不欢'},{value:'sweet',emoji:'🍰',label:'偏甜口'},{value:'healthy',emoji:'🥗',label:'清淡健康'}] },
  { key:'has_pet', dimension:'生活习惯', emoji:'🐾', text:'你对养宠物的态度？', options:[{value:'love',emoji:'😍',label:'超爱，想养猫/狗'},{value:'ok',emoji:'🙂',label:'还行，不排斥'},{value:'no',emoji:'🤧',label:'过敏/不太喜欢'}] },
  { key:'exercise_habit', dimension:'生活习惯', emoji:'💪', text:'你的运动频率？', options:[{value:'daily',emoji:'🏋️',label:'几乎每天'},{value:'weekly',emoji:'🏃',label:'每周 2-3 次'},{value:'rarely',emoji:'🧘',label:'偶尔动一动'},{value:'never',emoji:'🛋️',label:'基本不动'}] },
  { key:'tidiness', dimension:'生活习惯', emoji:'🧹', text:'你的整洁程度？', options:[{value:'very_tidy',emoji:'✨',label:'非常整洁，一尘不染'},{value:'tidy',emoji:'🧼',label:'比较整洁'},{value:'casual',emoji:'🤷',label:'一般般，过得去'},{value:'messy',emoji:'🌀',label:'比较随意，找得到就行'}] },
  { key:'screen_time', dimension:'生活习惯', emoji:'📱', text:'你每天刷手机的时间？', options:[{value:'low',emoji:'📵',label:'2小时以内'},{value:'medium',emoji:'📱',label:'3-5小时'},{value:'high',emoji:'📲',label:'5-8小时'},{value:'very_high',emoji:'🖥️',label:'8小时以上，离不开了'}] },

  // === 约会偏好 ===
  { key:'ideal_first_date', dimension:'约会偏好', emoji:'🌹', text:'第一次约会，你更想去？', options:[{value:'cafe',emoji:'☕',label:'安静的咖啡馆'},{value:'walk',emoji:'🚶',label:'边走边聊、逛街'},{value:'activity',emoji:'🎳',label:'一起做个小活动'},{value:'meal',emoji:'🍜',label:'吃一顿好吃的'}] },
  { key:'when_to_date', dimension:'约会偏好', emoji:'📅', text:'你希望认识多久后确定关系？', options:[{value:'fast',emoji:'⚡',label:'感觉对了就行'},{value:'one_month',emoji:'📆',label:'聊一个月左右'},{value:'three_months',emoji:'🗓️',label:'两三个月再说'},{value:'slow',emoji:'🐢',label:'慢慢来不着急'}] },

  // ===== 多选题（第 21-30 题）=====

  // === 性格自述 ===
  { key:'self_description', dimension:'性格特质', emoji:'🪞', text:'你觉得自己的关键词是？（多选）', multi:true, options:[{value:'warm',emoji:'🔥',label:'温暖'},{value:'humor',emoji:'😂',label:'幽默'},{value:'quiet',emoji:'🤫',label:'安静'},{value:'active',emoji:'🏃',label:'活泼'},{value:'careful',emoji:'🔍',label:'细心'},{value:'creative',emoji:'💡',label:'有创意'},{value:'reliable',emoji:'🛡️',label:'靠谱'},{value:'romantic',emoji:'🌹',label:'浪漫'}] },

  // === 兴趣爱好 ===
  { key:'hobbies', dimension:'兴趣爱好', emoji:'🎨', text:'业余时间喜欢做什么？（多选）', multi:true, options:[{value:'music',emoji:'🎵',label:'听音乐/演奏'},{value:'movies',emoji:'🎬',label:'看电影/追剧'},{value:'sports',emoji:'⚽',label:'运动健身'},{value:'games',emoji:'🎮',label:'打游戏'},{value:'reading',emoji:'📚',label:'读书'},{value:'cooking',emoji:'🍳',label:'做饭/烘焙'},{value:'photo',emoji:'📸',label:'摄影'},{value:'travel',emoji:'🗺️',label:'旅行'}] },
  { key:'campus_activities', dimension:'兴趣爱好', emoji:'🏫', text:'你参加过哪些校园活动？（多选）', multi:true, options:[{value:'club',emoji:'🎭',label:'社团'},{value:'volunteer',emoji:'🤝',label:'志愿者'},{value:'competition',emoji:'🏆',label:'学科竞赛'},{value:'sports_event',emoji:'⚽',label:'运动会/体育赛事'},{value:'art_show',emoji:'🎤',label:'文艺演出'},{value:'none',emoji:'😌',label:'基本没参加过'}] },
  { key:'entertainment', dimension:'兴趣爱好', emoji:'🎭', text:'你喜欢的娱乐方式？（多选）', multi:true, options:[{value:'concert',emoji:'🎵',label:'看演唱会/live'},{value:'board_game',emoji:'🎲',label:'桌游/剧本杀'},{value:'kTV',emoji:'🎤',label:'KTV'},{value:'exhibition',emoji:'🖼️',label:'看展/博物馆'},{value:'cafe_crawl',emoji:'☕',label:'探店/咖啡馆'},{value:'night_market',emoji:'🏮',label:'夜市/逛街'}] },
  { key:'music_style', dimension:'兴趣爱好', emoji:'🎧', text:'你喜欢什么类型的音乐？（多选）', multi:true, options:[{value:'pop',emoji:'🎤',label:'流行'},{value:'rock',emoji:'🎸',label:'摇滚'},{value:'rap',emoji:'🎤',label:'说唱/Hip-hop'},{value:'folk',emoji:'🪕',label:'民谣'},{value:'classical',emoji:'🎻',label:'古典/纯音乐'},{value:'electronic',emoji:'🎹',label:'电子音乐'},{value:'r_and_b',emoji:'🎷',label:'R&B/爵士'},{value:'none',emoji:'🔇',label:'不太听歌'}] },
  { key:'travel_style', dimension:'兴趣爱好', emoji:'🧳', text:'你喜欢的旅行方式？（多选）', multi:true, options:[{value:'backpack',emoji:'🎒',label:'穷游背包'},{value:'food_trip',emoji:'🍜',label:'美食之旅'},{value:'culture',emoji:'🏛️',label:'文化古迹'},{value:'nature',emoji:'🏔️',label:'自然风光'},{value:'city',emoji:'🏙️',label:'城市探索'},{value:'staycation',emoji:'🏨',label:'度假酒店躺平'}] },
  { key:'study_habits', dimension:'兴趣爱好', emoji:'📚', text:'你的学习习惯是？（多选）', multi:true, options:[{value:'library',emoji:'📖',label:'泡图书馆'},{value:'group',emoji:'👥',label:'小组讨论'},{value:'online',emoji:'💻',label:'网课自学'},{value:'cram',emoji:'🔥',label:'考前突击'},{value:'note_taking',emoji:'✍️',label:'认真做笔记'},{value:'discuss',emoji:'🗣️',label:'跟老师交流'}] },

  // === 择偶偏好 ===
  { key:'target_traits', dimension:'择偶偏好', emoji:'💝', text:'你希望对方有什么特质？（多选）', multi:true, options:[{value:'humor',emoji:'😂',label:'幽默有趣'},{value:'gentle',emoji:'🌸',label:'温柔体贴'},{value:'ambitious',emoji:'🚀',label:'上进有目标'},{value:'honest',emoji:'💎',label:'真诚坦率'},{value:'smart',emoji:'🧠',label:'聪明有见识'},{value:'caring',emoji:'🤗',label:'会照顾人'}] },
  { key:'deal_breakers', dimension:'择偶偏好', emoji:'🚩', text:'你最不能接受对方的哪些行为？（多选）', multi:true, options:[{value:'lying',emoji:'🤥',label:'说谎/不诚实'},{value:'cold',emoji:'🧊',label:'冷暴力'},{value:'messy_p',emoji:'🌀',label:'太邋遢'},{value:'clingy',emoji:'📎',label:'太黏人/控制欲强'},{value:'cheap',emoji:'🪙',label:'太抠门'},{value:'flirty',emoji:'😏',label:'跟异性暧昧不清'}] },
  { key:'date_activities', dimension:'约会偏好', emoji:'🎉', text:'理想的约会活动？（多选）', multi:true, options:[{value:'movie',emoji:'🎬',label:'看电影'},{value:'dinner',emoji:'🕯️',label:'烛光晚餐'},{value:'sport',emoji:'🏸',label:'一起运动'},{value:'game',emoji:'🎮',label:'打游戏/桌游'},{value:'walk_p',emoji:'🌅',label:'散步/看日落'},{value:'cook',emoji:'🍳',label:'一起做饭'}] },
]

function isSelected(step: number, value: string): boolean {
  const q = questions[step]
  if (q.multi) {
    return ((answers[q.key] as string[]) || []).includes(value)
  }
  return answers[q.key] === value
}

function multiCount(step: number): number {
  const q = questions[step]
  return ((answers[q.key] as string[]) || []).length
}

function selectSingle(value: string) {
  answers[questions[currentStep.value].key] = value
  if (currentStep.value < questions.length - 1) {
    setTimeout(() => { currentStep.value++ }, 350)
  }
}

function toggleMulti(value: string) {
  const key = questions[currentStep.value].key
  const arr = (answers[key] as string[]) || []
  const idx = arr.indexOf(value)
  if (idx >= 0) {
    arr.splice(idx, 1)
  } else {
    arr.push(value)
  }
  answers[key] = [...arr]
}

function next() {
  if (currentStep.value < questions.length - 1) {
    currentStep.value++
  } else {
    submit()
  }
}

function prev() {
  if (currentStep.value > 0) currentStep.value--
}

async function submit() {
  try {
    const res = await questionnaireApi.patch(answers)
    completion.value = res.data.completion_rate
    await auth.fetchProfile()
    completed.value = true
  } catch { toast.error('提交失败，请重试') }
}

async function goToMatch() {
  await router.push('/app/match')
}

onMounted(async () => {
  try {
    const res = await questionnaireApi.get()
    if (res.data.answers) Object.assign(answers, res.data.answers)
  } catch {}
})
</script>

<style scoped>
.q-slide-enter-active, .q-slide-leave-active { transition: all 0.3s ease; }
.q-slide-enter-from { opacity: 0; transform: translateX(30px); }
.q-slide-leave-to { opacity: 0; transform: translateX(-30px); }
</style>
