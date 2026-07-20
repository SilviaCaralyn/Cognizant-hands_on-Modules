import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, c) => sum + (c.credits || 0), 0)
  )

  function enroll(course) {
    const alreadyEnrolled = enrolledCourses.value.some((c) => c.id === course.id)
    if (!alreadyEnrolled) enrolledCourses.value.push(course)
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((c) => c.id !== courseId)
  }

  // Step 149: advanced action combining an API call + state update in one step
  async function fetchAndEnroll(courseId) {
    const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`)
    if (!res.ok) throw new Error('Course not found')
    const post = await res.json()
    enroll({
      id: post.id,
      name: post.title.slice(0, 24),
      code: `CS${100 + post.id}`,
      credits: 3,
      grade: 'TBD',
    })
  }

  function $reset() {
    enrolledCourses.value = []
  }

  return { enrolledCourses, totalCredits, enroll, unenroll, fetchAndEnroll, $reset }
})
