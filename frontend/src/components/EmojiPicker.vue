<template>
  <div class="relative inline-block">
    <button @click="showPicker = !showPicker" type="button"
      class="text-text-sub active:scale-90 transition-transform p-1">
      <span class="text-lg"> </span>
    </button>
    <div v-if="showPicker" @click.self="showPicker = false"
      class="fixed inset-0 z-50" />
    <div v-if="showPicker"
      class="absolute bottom-full mb-2 left-0 z-50 bg-white rounded-2xl shadow-xl border border-gray-100 p-3 w-72 animate-slide-up">
      <div class="flex gap-1 mb-2 overflow-x-auto pb-1">
        <button v-for="(cat, idx) in categories" :key="idx"
          @click="activeCategory = idx"
          class="px-2.5 py-1 rounded-lg text-xs font-bold whitespace-nowrap transition-all shrink-0"
          :class="activeCategory === idx ? 'bg-pink-pale text-pink-heart' : 'text-text-sub hover:bg-gray-50'">
          {{ cat.name }}
        </button>
      </div>
      <div class="grid grid-cols-8 gap-0.5 max-h-40 overflow-y-auto">
        <button v-for="emoji in categories[activeCategory].emojis" :key="emoji"
          @click="selectEmoji(emoji)"
          class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-pink-pale active:scale-90 transition-all text-lg">
          {{ emoji }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'select', emoji: string): void
}>()

const showPicker = ref(false)
const activeCategory = ref(0)

const categories = [
  { name: '常用', emojis: ['❤️',' ','✨',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','✊',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','⭐'] },
  { name: '表情', emojis: [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] },
  { name: '手势', emojis: [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','✊',' ','✋',' ',' ','✌️',' ','☝️',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] },
  { name: '动物', emojis: [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] },
  { name: '食物', emojis: [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','☕',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] },
  { name: '活动', emojis: [' ','⚽',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] },
]

function selectEmoji(emoji: string) {
  emit('select', emoji)
  showPicker.value = false
}
</script>
