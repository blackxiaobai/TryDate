<template>
  <div class="page-container px-4 pt-8 pb-10">
    <div class="flex items-center gap-3 mb-6">
      <button @click="$router.back()" class="w-9 h-9 rounded-xl bg-white/70 flex items-center justify-center shadow-sm">
        <ArrowLeftIcon class="w-5 h-5 text-text-main" />
      </button>
      <h1 class="text-xl font-black text-text-main">隐私政策</h1>
    </div>

    <div class="card space-y-4 text-sm text-text-main leading-relaxed">
      <p class="text-text-sub text-xs">最后更新日期：2026年5月17日</p>

      <h2 class="text-base font-black text-text-main">一、信息收集</h2>
      <p>我们收集以下信息以提供匹配服务：</p>
      <p>1. <strong>注册信息</strong>：邮箱地址、昵称、性别、出生年份、密码（加密存储）。</p>
      <p>2. <strong>个人资料</strong>：年级、专业方向、个人简介、头像。</p>
      <p>3. <strong>问卷数据</strong>：灵魂问卷的回答内容，用于匹配算法计算。</p>
      <p>4. <strong>使用数据</strong>：匹配记录、聊天消息、动态发布与互动数据。</p>

      <h2 class="text-base font-black text-text-main">二、信息使用</h2>
      <p>我们使用收集的信息用于：</p>
      <p>1. 提供核心匹配服务，通过算法为用户推荐契合的对象。</p>
      <p>2. 维护平台安全，检测和防止欺诈、滥用等违规行为。</p>
      <p>3. 改善服务质量，优化匹配算法和用户体验。</p>
      <p>4. 发送必要的服务通知，如匹配结果提醒、验证码等。</p>

      <h2 class="text-base font-black text-text-main">三、信息保护</h2>
      <p>1. 用户密码采用加密算法存储，平台无法查看明文密码。</p>
      <p>2. 聊天消息仅在匹配成功后才可查看，匹配未成功时双方头像和昵称均被隐藏。</p>
      <p>3. 匹配双方在匹配成功之前，无法查看对方的头像照片。</p>
      <p>4. 用户可选择匿名发布动态，匿名状态下其他用户无法看到发布者身份。</p>
      <p>5. 聊天记录每周自动清空，不会长期保留。</p>

      <h2 class="text-base font-black text-text-main">四、信息共享</h2>
      <p>1. 我们不会向第三方出售、出租或交易用户的个人信息。</p>
      <p>2. 仅在以下情况下可能共享信息：</p>
      <p class="pl-4">- 获得用户明确同意的情况下</p>
      <p class="pl-4">- 根据法律法规或政府主管部门要求</p>
      <p class="pl-4">- 为保护平台及用户安全所必需的情况</p>

      <h2 class="text-base font-black text-text-main">五、用户权利</h2>
      <p>1. 用户可随时查看和修改个人资料信息。</p>
      <p>2. 用户可使用举报功能报告不当行为。</p>
      <p>3. 用户可使用拉黑功能屏蔽不想互动的用户。</p>
      <p>4. 用户可选择匿名发布动态和评论。</p>
      <p>5. 用户可通过联系客服申请注销账号，注销后相关数据将被删除。</p>

      <h2 class="text-base font-black text-text-main">六、数据存储</h2>
      <p>1. 用户数据存储于安全的服务器环境中。</p>
      <p>2. 聊天消息在 7 天后自动清除。</p>
      <p>3. 注销账号后，个人数据将在合理时间内被删除。</p>

      <h2 class="text-base font-black text-text-main">七、未成年人保护</h2>
      <p>本平台仅面向年满 18 周岁的在校大学生。我们不会故意收集未成年人的个人信息。</p>

      <h2 class="text-base font-black text-text-main">八、政策更新</h2>
      <p>我们可能会不时更新本隐私政策。更新后的政策将在平台上公布，继续使用本平台即表示用户接受更新后的政策。</p>

      <h2 class="text-base font-black text-text-main">九、联系我们</h2>
      <p>如对本隐私政策有任何疑问或建议，请通过平台内"意见反馈"功能联系我们。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeftIcon } from 'lucide-vue-next'
</script>
