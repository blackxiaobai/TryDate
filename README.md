<div align="center">

<img src="https://img.shields.io/badge/version-v1.2-FF6B8A?style=for-the-badge" alt="version"/>
<img src="https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white" alt="django"/>
<img src="https://img.shields.io/badge/Vue-3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="vue"/>
<img src="https://img.shields.io/badge/WebSocket-实时通信-FF6B8A?style=for-the-badge" alt="websocket"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="postgresql"/>
<img src="https://img.shields.io/badge/Redis-5-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="redis"/>

<br/><br/>

# 💝 TryDate — 校园心动匹配平台

### *"在最好的年纪，遇见刚刚好的你"*

一款专为高校在校生设计的心动匹配与交友平台。
不靠颜值滤镜，通过趣味问卷、价值观匹配和温暖的互动设计，
帮你遇见那个「感觉刚刚好」的人。

</div>

---

## ✨ 功能一览

| 模块 | 功能 |
|------|------|
| 🔐 **注册登录** | 邮箱验证码 + 密码双模式登录，邮箱格式校验，JWT 鉴权 |
| 🧠 **灵魂问卷** | 30 道趣味题（含 10 道多选），五维度性格画像 |
| 💘 **智能匹配** | 按需触发匹配，每人每周 2 次机会，契合度即时计算 |
| 🤝 **双向确认** | 心动 / 再想想，双方都选心动才解锁聊天，拒绝不消耗次数 |
| 💬 **实时聊天** | WebSocket 驱动，支持文字 & 图片消息、打字提示 |
| 📝 **话题动态** | 支持匿名发布，点赞互动 |
| 🚩 **举报拉黑** | 一键举报 + 拉黑屏蔽，保障安全 |
| ⚙️ **管理后台** | Vue 管理面板，用户/匹配/动态/举报全面管理 |

---

## 🏗 技术栈

```
后端          Django 5.0 + Django REST Framework
实时通信      Django Channels + Daphne (ASGI) + WebSocket
数据库        PostgreSQL
缓存 & 频道   Redis
身份认证      JWT (djangorestframework-simplejwt)
邮件服务      Resend API（HTTP，不受端口限制）
前端          Vue 3 + TypeScript + Vite + TailwindCSS
状态管理      Pinia
路由          Vue Router 4 (路由守卫)
UI 组件      Lucide Icons + vue3-toastify
匹配算法      Gale-Shapley 双向稳定匹配
部署          Render（全栈） + 自定义域名
```

---

## 📁 项目结构

```
TryDate/
├── backend/
│   ├── config/              # Django 配置 (settings, urls, asgi)
│   ├── users/               # 用户注册 / 登录 / 资料 / 邮箱验证码
│   ├── questionnaire/       # 灵魂问卷（30 题，五维度 JSON 存储）
│   ├── matching/            # 按需匹配 + Gale-Shapley 算法 + 契合度计算
│   ├── chat/                # WebSocket 实时聊天 + 举报拉黑
│   ├── posts/               # 话题动态（发布 / 点赞 / 匿名）
│   ├── admin_api/           # 管理后台 API
│   ├── build.sh             # Render 部署构建脚本
│   ├── runtime.txt          # Python 版本指定
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/             # Axios HTTP 封装 + API 方法
│   │   ├── stores/          # Pinia 状态管理 (auth)
│   │   ├── router/          # Vue Router 路由 + 守卫
│   │   ├── layouts/         # 布局组件 (AppLayout, AdminLayout)
│   │   └── pages/           # 页面组件
│   │       └── admin/       # 管理后台页面
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── package.json
└── README.md
```

---

## 🚀 本地开发

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入数据库密码等配置

# 执行迁移 & 创建管理员
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 启动（支持 WebSocket）
daphne -p 8000 config.asgi:application
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173

### 管理员入口

登录后点击导航栏「管理」按钮，或访问 `/admin`。

---

## 🌐 部署上线

项目支持全栈部署到 [Render](https://render.com)（免费方案）：

```
Render Web Service
├── Daphne ASGI 后端
├── 静态文件 (WhiteNoise)
├── Vue SPA 前端 (构建后由 Django serve)
├── PostgreSQL (Render 免费)
└── Redis (Render 免费)
```

### 部署步骤

1. Fork 本仓库到你的 GitHub
2. 在 Render 创建 Web Service，Root Directory 设为 `backend`
3. Build Command: `bash build.sh`
4. Start Command: `daphne -b 0.0.0.0 -p $PORT config.asgi:application`
5. 添加 PostgreSQL 和 Redis 实例
6. 设置环境变量（见下方清单）
7. （可选）绑定自定义域名，添加 CNAME 记录指向 `trydate.onrender.com`

### 环境变量

| 变量 | 说明 |
|------|------|
| `SECRET_KEY` | Django 密钥（随机生成） |
| `DEBUG` | `False`（生产环境） |
| `ALLOWED_HOSTS` | 你的域名，逗号分隔 |
| `CORS_ALLOWED_ORIGINS` | 前端域名，逗号分隔 |
| `CSRF_TRUSTED_ORIGINS` | 前端域名，逗号分隔 |
| `DATABASE_URL` | Render PostgreSQL 连接串 |
| `REDIS_URL` | Render Redis 连接串 |
| `RESEND_API_KEY` | Resend 邮件服务 API Key |
| `EMAIL_HOST` | SMTP 服务器（本地开发用） |
| `EMAIL_HOST_USER` | 发件邮箱 |
| `EMAIL_HOST_PASSWORD` | 邮箱授权码 |

> **邮件服务说明**：生产环境使用 [Resend](https://resend.com) HTTP API 发送验证码邮件，不受 Render 端口限制。需要在 Resend 绑定发信域名并添加 DNS 记录。

构建脚本会自动安装前端依赖、构建 Vue 项目、执行数据库迁移并创建管理员账号。

---

## 🧮 匹配系统

### 按需匹配

用户点击「开始匹配」按钮，系统即时为用户找到最佳契合对象。

- 每人每周最多成功匹配 **2 次**
- 选「再想想」不消耗次数，可继续寻找
- 双方都选「心动」后才计为一次成功匹配
- 每周一自动重置匹配次数

### 匹配算法

采用 **两阶段方案**：

1. **契合度计算** — 基于 30 道问卷答案，五维加权评分（满分 100）
2. **Gale-Shapley 双向稳定匹配** — 保证匹配结果的稳定性，消除不稳定配对

```
总契合度 = 基础偏好 × 15%
         + 爱情观 & 价值观 × 40%
         + 生活习惯 × 25%
         + 兴趣爱好 × 15%
         + 约会偏好 × 5%
```

---

## 📡 API 概览

<details>
<summary><b>👤 用户 /api/users/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/send-code/` | 发送邮箱验证码 |
| POST | `/register/` | 注册（邮箱 + 密码 + 验证码） |
| POST | `/login/` | 验证码登录 |
| POST | `/login/password/` | 密码登录 |
| POST | `/token/refresh/` | 刷新 JWT Token |
| GET/PATCH | `/profile/` | 获取 / 更新个人资料 |

</details>

<details>
<summary><b>📋 问卷 /api/questionnaire/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 获取问卷答案与完成度 |
| PATCH | `/` | 提交 / 更新答案（增量合并） |

</details>

<details>
<summary><b>💘 匹配 /api/match/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/request/` | 请求匹配，系统推荐最佳对象 |
| GET | `/current/` | 当前匹配 + 契合度报告 |
| POST | `/{id}/respond/` | 心动 / 再想想 |
| GET | `/history/` | 历史匹配记录 |

</details>

<details>
<summary><b>💬 聊天 /api/chat/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/rooms/` | 聊天室列表 |
| GET | `/rooms/{id}/messages/` | 消息历史 |
| POST | `/rooms/{id}/upload/` | 上传图片 |
| POST | `/report/` | 举报用户 |
| POST | `/block/{user_id}/` | 拉黑用户 |

</details>

<details>
<summary><b>📝 动态 /api/posts/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 动态列表 |
| POST | `/create/` | 发布动态 |
| POST | `/{id}/like/` | 点赞 / 取消点赞 |
| DELETE | `/{id}/delete/` | 删除动态 |

</details>

---

## 📄 License

[MIT](LICENSE) © 2026 TryDate

---

<div align="center">
  <sub>Made with 💝 for campus love</sub>
</div>
