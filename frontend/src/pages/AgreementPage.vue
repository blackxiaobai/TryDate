<template>
  <div class="page-container px-4 pt-8 pb-10">
    <div class="flex items-center gap-3 mb-6">
      <button @click="$router.back()" class="w-9 h-9 rounded-xl bg-white/70 flex items-center justify-center shadow-sm">
        <ArrowLeftIcon class="w-5 h-5 text-text-main" />
      </button>
      <h1 class="text-xl font-black text-text-main">用户协议</h1>
    </div>

    <div class="card space-y-4 text-sm text-text-main leading-relaxed">
      <p class="text-text-sub text-xs">最后更新日期：2026年5月17日</p>

      <h2 class="text-base font-black text-text-main">一、服务说明</h2>
      <p>TryDate（以下简称"本平台"）是一个面向在校大学生的校园恋爱匹配社交平台。本平台通过灵魂问卷匹配算法，为用户提供个性化的交友匹配服务。</p>

      <h2 class="text-base font-black text-text-main">二、用户注册</h2>
      <p>1. 用户须为在校大学生或研究生，使用学校邮箱进行注册验证。</p>
      <p>2. 用户应提供真实、准确、完整的个人资料，包括但不限于昵称、性别、出生年份等信息。</p>
      <p>3. 每个邮箱地址仅可注册一个账户，禁止创建多个账号。</p>
      <p>4. 用户须妥善保管账户密码，因用户自身原因导致的账户安全问题，本平台不承担责任。</p>

      <h2 class="text-base font-black text-text-main">三、用户行为规范</h2>
      <p>1. 用户在使用本平台服务时，须遵守中华人民共和国相关法律法规。</p>
      <p>2. 禁止发布以下内容：</p>
      <p class="pl-4">- 违反国家法律法规的内容</p>
      <p class="pl-4">- 涉及色情、暴力、赌博等不良信息</p>
      <p class="pl-4">- 侮辱、诽谤、骚扰他人的内容</p>
      <p class="pl-4">- 虚假信息或冒充他人身份</p>
      <p class="pl-4">- 广告、推广等商业信息</p>
      <p>3. 用户之间应互相尊重，文明交流。禁止任何形式的骚扰、威胁或不当行为。</p>
      <p>4. 禁止利用本平台从事任何违法违规活动。</p>

      <h2 class="text-base font-black text-text-main">四、匹配服务</h2>
      <p>1. 本平台基于用户填写的灵魂问卷进行智能匹配，匹配结果仅供参考。</p>
      <p>2. 每位用户每周最多可进行 2 次匹配，接受匹配后扣除 1 次机会。</p>
      <p>3. 匹配双方均有权选择接受或拒绝匹配提议。</p>
      <p>4. 匹配成功后，双方可进入聊天室进行交流。</p>

      <h2 class="text-base font-black text-text-main">五、知识产权</h2>
      <p>本平台的所有内容，包括但不限于文字、图片、软件、算法等，均受知识产权法律保护。未经授权，用户不得复制、修改、传播本平台的任何内容。</p>

      <h2 class="text-base font-black text-text-main">六、免责声明</h2>
      <p>1. 本平台仅提供社交匹配服务，不对用户之间的线下交往行为负责。</p>
      <p>2. 因用户自身行为导致的任何纠纷或损失，本平台不承担责任。</p>
      <p>3. 因不可抗力或本平台无法控制的原因导致的服务中断，本平台不承担责任。</p>

      <h2 class="text-base font-black text-text-main">七、协议修改</h2>
      <p>本平台有权根据需要修改本协议内容，修改后的协议将在平台上公布。继续使用本平台即表示用户接受修改后的协议。</p>

      <h2 class="text-base font-black text-text-main">八、联系方式</h2>
      <p>如对本协议有任何疑问，请通过平台内"意见反馈"功能联系我们。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeftIcon } from 'lucide-vue-next'
</script>
