<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import CourseCard from '../components/CourseCard.vue'
import { useEnrollmentStore } from '../stores/enrollment.js'

const courses = ref([])
const searchTerm = ref('')
const loading = ref(true)
const error = ref(null)
const router = useRouter()
const store = useEnrollmentStore()

const FALLBACK_META = [
  { credits: 4, grade: 'A' },
  { credits: 4, grade: 'B+' },
  { credits: 3, grade: 'A-' },
  { credits: 4, grade: 'A' },
  { credits: 3, grade: 'B' },
]

onMounted(async () => {
  try {
    const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
    if (!res.ok) throw new Error(`Request failed with status ${res.status}`)
    const posts = await res.json()
    courses.value = posts.map((post, index) => ({
      id: post.id,
      name: post.title.slice(0, 24),
      code: `CS${100 + index}`,
      credits: FALLBACK_META[index % FALLBACK_META.length].credits,
      grade: FALLBACK_META[index % FALLBACK_META.length].grade,
    }))
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})

const filteredCourses = computed(() =>
  courses.value.filter((c) => c.name.toLowerCase().includes(searchTerm.value.toLowerCase()))
)

function handleEnroll(course) {
  store.enroll(course)
  router.push('/profile') // Step 115
}
</script>

<template>
  <section aria-labelledby="courses-heading">
    <h2 id="courses-heading">Courses</h2>

    <label for="search">Search courses</label>
    <input id="search" v-model="searchTerm" placeholder="Search courses..." />

    <p v-if="loading" role="status">Loading...</p>
    <p v-if="error" role="alert">Error: {{ error }}</p>

    <div class="course-grid" v-if="!loading && !error">
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        v-bind="course"
        @enroll="handleEnroll"
      />
    </div>
  </section>
</template>
