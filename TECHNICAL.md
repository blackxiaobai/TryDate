# TryDate 技术文档

## 项目概述

TryDate 是一款面向高校学生的心动匹配交友平台。区别于传统颜值驱动的交友软件，TryDate 通过 30 道趣味心理问卷（含 10 道多选题）构建用户五维性格画像，结合 Gale-Shapley 双向稳定匹配算法实现智能推荐，双方互选心动后自动解锁实时聊天。

**在线体验**：https://dlnu-love.top

---

## 技术架构

```
┌─────────────────────────────────────────────────┐
│                   用户浏览器                       │
│            Vue 3 SPA (HTTPS 访问)                 │
└───────────┬─────────────────────────┬────────────┘
            │ HTTP/REST               │ WebSocket
            ▼                         ▼
┌─────────────────────────────────────────────────┐
│              Daphne (ASGI Server)                 │
│         Django 5.0 + Django Channels              │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ REST API │ │ WebSocket│ │ WhiteNoise 静态   │  │
│  │ (DRF)    │ │ (Chat)   │ │ (Vue SPA 托管)   │  │
│  └────┬─────┘ └────┬─────┘ └──────────────────┘  │
└───────┼────────────┼─────────────────────────────┘
        │            │
   ┌────▼────┐  ┌────▼────┐
   │PostgreSQL│  │  Redis   │
   │ (数据)   │  │ (频道层)  │
   └─────────┘  └─────────┘
```

### 技术选型及理由

| 层级 | 技术 | 选型理由 |
|------|------|---------|
| 后端框架 | Django 5.0 | 成熟的 ORM、内置 Admin、安全机制完善 |
| API 层 | Django REST Framework | 序列化/分页/权限一站式解决方案 |
| 实时通信 | Django Channels + Daphne | 与 Django 生态无缝集成，原生 WebSocket 支持 |
| 数据库 | PostgreSQL | JSONField 支持灵活的问卷存储，事务可靠 |
| 缓存 & 频道 | Redis | Channels 频道层 + 缓存双用途 |
| 前端框架 | Vue 3 + TypeScript | Composition API 类型安全，开发效率高 |
| 构建工具 | Vite 5 | 极速 HMR，原生 ES Module |
| 样式 | TailwindCSS | 原子化 CSS，移动端优先设计 |
| 状态管理 | Pinia | Vue 官方推荐，TypeScript 友好 |
| 部署 | Render（全栈） | 免费 PostgreSQL + Redis + Web Service |
| 邮件服务 | Resend API | HTTP 发信，不受云平台 SMTP 端口封锁 |

---

## 核心功能模块

### 1. 用户认证系统

**登录方式**：邮箱 + 验证码 / 邮箱 + 密码

**技术要点**：
- 使用 `djangorestframework-simplejwt` 实现 JWT 无状态认证
- Access Token 有效期 7 天，Refresh Token 30 天，支持自动续签
- 前端 Axios 拦截器实现 401 自动刷新 Token，避免用户频繁登录
- 验证码通过 Resend HTTP API 发送，失败时回退到控制台日志

```
注册流程：
  前端 → POST /api/users/send-code/ → Resend API → 用户邮箱
  前端 → POST /api/users/register/ → 验证码校验 → 创建用户 → 返回 JWT
```

### 2. 灵魂问卷系统

**30 道题，五维度，10 道多选**

| 维度 | 题数 | 题型 | 权重 |
|------|------|------|------|
| 基础偏好 | 含在各维度 | 单选 | 15% |
| 爱情观 & 价值观 | 7 题 | 单选 | 40% |
| 生活习惯 | 7 题 | 单选 | 25% |
| 兴趣爱好 | 7 题 | 多选 + 单选 | 15% |
| 约会偏好 | 3 题 | 单选 + 多选 | 5% |

**技术要点**：
- 答案以 JSONField 存储，支持增量合并（PATCH），无需逐题提交
- 多选题答案存储为 JSON 数组，使用 Jaccard 相似度计算匹配度
- 前端单选题自动跳转下一题（350ms 动画过渡），多选题手动翻页
- 完成度实时计算，低于阈值无法参与匹配

```python
# 存储结构示例
{
    "personality_type": "ambivert",
    "love_priorities": "understanding",
    "hobbies": ["music", "travel", "photo"],
    "self_description": ["warm", "humor", "reliable"],
    ...
}
```

### 3. 智能匹配算法

采用**两阶段匹配方案**：

#### 阶段一：契合度计算

对任意两个用户，根据五维问卷答案计算 0-100 的契合度分数：

```python
总契合度 = 基础偏好 × 15%
         + 爱情观 & 价值观 × 40%    # 最高权重
         + 生活习惯 × 25%
         + 兴趣爱好 × 15%
         + 约会偏好 × 5%
```

各维度内部采用不同评分策略：
- **单选题**：相同答案 = 1.0，差 1 级 = 0.7，差 2 级 = 0.4
- **量表题**（空间需求、异地恋接受度）：`1 - |差值| / (最大值-1)`
- **多选题**：Jaccard 系数 `|A∩B| / |A∪B|`

#### 阶段二：Gale-Shapley 双向稳定匹配

经典算法保证：
- **稳定性**：不存在两个未匹配用户更偏好对方而非当前匹配对象
- **最优性**：对主动方（proposer）而言是所有稳定匹配中最优的

```python
def gale_shapley(proposers, receivers, scores):
    # proposers 按契合度降序排列偏好列表
    # receivers 按契合度降序排列偏好列表
    # 每轮 proposer 向未拒绝它的最高偏好 receiver 提出
    # receiver 保留最优提议，拒绝其余
    # 直到所有 proposer 都匹配或被所有人拒绝
    return {proposer_id: receiver_id}
```

### 4. 实时聊天系统

**技术栈**：Django Channels + WebSocket + Redis Channel Layer

**功能特性**：
- 文字消息 & 图片消息（Base64 传输）
- 实时在线状态和打字提示
- 配对成功自动创建聊天室 + 系统消息
- 举报 & 拉黑功能

**WebSocket 协议**：
```
ws://host/ws/chat/{room_id}/?token={jwt}

消息格式：
{ "type": "chat_message", "content": "你好", "msg_type": "text" }
{ "type": "typing" }  // 打字提示
```

**关键设计**：
- WebSocket 连接携带 JWT Token，通过自定义中间件验证
- 使用 Redis Channel Layer 实现多实例消息广播
- 聊天室通过 Match 记录关联，未匹配用户无法访问

### 5. 话题动态系统

- 支持匿名发布（不显示头像和昵称）
- 点赞 / 取消点赞（乐观更新 + 服务端幂等）
- 图片上传（Pillow 压缩处理）
- 分页加载（DRF PageNumberPagination）

---

## 数据库设计

### 核心模型关系

```
User (1) ──→ (1) Questionnaire
User (1) ──→ (N) Post
User (1) ──→ (N) PostLike
User (N) ──→ (N) User  [through Match]
Match (1) ──→ (1) ChatRoom
ChatRoom (1) ──→ (N) Message
User (N) ──→ (N) User  [through BlackList]
```

### 关键模型

```python
class User(AbstractUser):
    nickname: str
    gender: str            # male / female / other
    avatar: ImageField
    bio: str
    birthday: date
    height: int            # cm
    grade: str             # 大一/大二/大三/大四/研一/研二
    college_direction: str # 文科/理科/工科/艺术/其他
    relationship_status: str
    questionnaire_completion: int  # 0-100

class Match(models.Model):
    user_a: FK → User
    user_b: FK → User
    compatibility_score: float     # 契合度
    dimension_scores: JSON         # 五维分项
    highlights: JSON               # 匹配亮点
    user_a_action: enum            # liked / passed / null
    user_b_action: enum
    status: enum                   # pending / matched / missed

class ChatRoom(models.Model):
    match: OneToOneField → Match
    created_at: datetime

class Message(models.Model):
    chat_room: FK → ChatRoom
    sender: FK → User (null = 系统消息)
    content: text
    msg_type: enum                 # text / image / system
```

---

## 部署架构

### 全栈 Render 部署

```
GitHub (代码仓库)
  │
  │  git push
  ▼
Render Web Service (自动构建)
  │
  ├── build.sh
  │   ├── pip install -r requirements.txt
  │   ├── cd ../frontend && npm install && npm run build
  │   ├── cp ../frontend/dist frontend-dist
  │   ├── python manage.py migrate
  │   ├── python manage.py collectstatic
  │   └── 创建默认管理员
  │
  ├── Daphne 启动
  │   └── daphne -b 0.0.0.0 -p $PORT config.asgi:application
  │
  ├── WhiteNoise 中间件 → 静态文件 (Django Admin)
  ├── 自定义 URL → Vite 资源 (前端 CSS/JS)
  ├── SPA 兜底路由 → index.html (Vue Router)
  │
  ├── PostgreSQL (Render 免费)
  └── Redis (Render 免费)
```

### 自定义域名

- 阿里云注册域名 `dlnu-love.top`
- CNAME 记录指向 `trydate.onrender.com`
- Django `ALLOWED_HOSTS` + `CSRF_TRUSTED_ORIGINS` 配置

### 邮件服务

- 生产环境：Resend API（HTTP 协议，绕过 Render SMTP 封锁）
- 需在 Resend 绑定域名 + DNS 验证（DKIM/SPF/DMARC）
- 发送失败自动回退到控制台日志，保证功能可用

---

## 遇到的技术挑战

### 1. Render 封锁出站 SMTP

**问题**：Render 免费版禁止出站 SMTP 端口，`Network is unreachable`

**解决**：引入 Resend HTTP API 发送邮件，设置 5 秒 Socket 超时 + 异常捕获兜底

### 2. psycopg2 安装失败

**问题**：Render Python 3.14 环境下 `psycopg2-binary==2.9.9` 无对应 wheel

**解决**：移除版本锁定 `psycopg2-binary>=2.9.9`，指定 `runtime.txt` 为 Python 3.11

### 3. 前端静态资源 502

**问题**：SPA 兜底路由拦截了 `/assets/*` 请求，返回 index.html

**解决**：添加 `serve_asset` 视图直接从 `frontend-dist/assets/` 返回文件，排除在兜底路由之外

### 4. JWT Token 自动续签

**问题**：401 导致无限重试循环

**解决**：Axios 拦截器添加 `isRefreshing` 锁 + `_retry` 标记，刷新失败则跳转登录

---

## 项目亮点（面试总结）

1. **全栈能力**：独立完成前后端 + 部署，从 0 到 1 的完整项目
2. **算法设计**：实现 Gale-Shapley 稳定匹配算法，五维加权契合度评分
3. **实时通信**：WebSocket 聊天系统，Redis 频道层消息广播
4. **工程实践**：JWT 鉴权、CORS 配置、SPA 路由、静态文件优化
5. **问题解决**：解决 SMTP 封锁、Python 兼容性、MIME 类型等生产环境问题
6. **部署运维**：全栈 Render 部署、自定义域名、CI/CD 自动构建
