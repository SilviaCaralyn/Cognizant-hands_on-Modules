<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment.js'

const route = useRoute()
const router = useRouter()
const store = useEnrollmentStore()

const course = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${route.params.id}`)
    if (!res.ok) throw new Error('Not found')
    const post = await res.json()
    course.value = {
      id: post.id,
      name: post.title.slice(0, 30),
      code: `CS${100 + Number(route.params.id)}`,
      credits: 3,
      grade: 'B+',
    }
  } catch {
    course.value = null
  } finally {
    loading.value = false
  }
})

function handleEnroll() {
  store.enroll(course.value)
  router.push('/profile')
}
</script>

<template>
  <p v-if="loading" role="status">Loading course...</p>
  <p v-else-if="!course" role="alert">Course not found.</p>
  <section v-else>
    <h2>{{ course.name }}</h2>
    <p>{{ course.code }} — {{ course.credits }} credits</p>
    <p>Grade: {{ course.grade }}</p>
    <button @click="handleEnroll">Enroll</button>
  </section>
</template>
