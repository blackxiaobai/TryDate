import http from './http'

export const userApi = {
  sendCode: (target: string, code_type: 'email' | 'phone') =>
    http.post('/users/send-code/', { target, code_type }),
  register: (data: object) => http.post('/users/register/', data),
  login: (data: object) => http.post('/users/login/', data),
  loginWithPassword: (email: string, password: string) =>
    http.post('/users/login/password/', { email, password }),
  getProfile: () => http.get('/users/profile/'),
  updateProfile: (data: object) => http.patch('/users/profile/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
}

export const questionnaireApi = {
  get: () => http.get('/questionnaire/'),
  patch: (answers: object) => http.patch('/questionnaire/', { answers }),
}

export const matchApi = {
  current: () => http.get('/match/current/'),
  respond: (id: number, action: 'liked' | 'passed') =>
    http.post(`/match/${id}/respond/`, { action }),
  history: () => http.get('/match/history/'),
}

export const chatApi = {
  rooms: () => http.get('/chat/rooms/'),
  messages: (roomId: number) => http.get(`/chat/rooms/${roomId}/messages/`),
  uploadImage: (roomId: number, formData: FormData) =>
    http.post(`/chat/rooms/${roomId}/upload/`, formData),
  report: (data: object) => http.post('/chat/report/', data),
  block: (userId: string) => http.post(`/chat/block/${userId}/`),
  unblock: (userId: string) => http.delete(`/chat/unblock/${userId}/`),
}

export const postsApi = {
  list: () => http.get('/posts/'),
  create: (data: { content: string; is_anonymous: boolean }) =>
    http.post('/posts/create/', data),
  like: (id: number) => http.post(`/posts/${id}/like/`),
  delete: (id: number) => http.delete(`/posts/${id}/delete/`),
}

export const adminApi = {
  dashboard: () => http.get('/admin/dashboard/'),
  users: (params?: Record<string, string>) => http.get('/admin/users/', { params }),
  banUser: (id: string) => http.post(`/admin/users/${id}/ban/`),
  unbanUser: (id: string) => http.post(`/admin/users/${id}/unban/`),
  matches: (params?: Record<string, string>) => http.get('/admin/matches/', { params }),
  posts: (params?: Record<string, string>) => http.get('/admin/posts/', { params }),
  hidePost: (id: number) => http.post(`/admin/posts/${id}/hide/`),
  restorePost: (id: number) => http.post(`/admin/posts/${id}/restore/`),
  reports: (params?: Record<string, string>) => http.get('/admin/reports/', { params }),
  resolveReport: (id: number, action: string) => http.post(`/admin/reports/${id}/resolve/`, { action }),
}
