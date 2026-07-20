import { apiClient } from './apiClient.js'

const FALLBACK_META = [
  { credits: 4, grade: 'A' },
  { credits: 4, grade: 'B+' },
  { credits: 3, grade: 'A-' },
  { credits: 4, grade: 'A' },
  { credits: 3, grade: 'B' },
]

function toCourse(post, index = 0) {
  return {
    id: post.id,
    name: post.title.slice(0, 24),
    code: `CS${100 + index}`,
    credits: FALLBACK_META[index % FALLBACK_META.length].credits,
    grade: FALLBACK_META[index % FALLBACK_META.length].grade,
  }
}

// Because of the response interceptor in apiClient.js, `data` here is already
// the parsed payload — callers never see the raw Axios response wrapper.
export async function getAllCourses() {
  const data = await apiClient.get('/posts?_limit=5')
  return data.map(toCourse)
}

export async function getCourseById(id) {
  const post = await apiClient.get(`/posts/${id}`)
  return toCourse(post, Number(id) - 1)
}

export async function enrollStudent(studentId, courseId) {
  // JSONPlaceholder doesn't have a real enrollment endpoint, so this POSTs
  // to /posts as a stand-in and returns a mock confirmation.
  const data = await apiClient.post('/posts', { studentId, courseId })
  return { success: true, enrollmentId: data.id, studentId, courseId }
}
