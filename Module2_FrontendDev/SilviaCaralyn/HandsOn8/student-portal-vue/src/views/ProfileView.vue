<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useEnrollmentStore } from '../stores/enrollment.js'

const store = useEnrollmentStore()
// storeToRefs preserves reactivity for state/getters (plain destructuring would not)
const { enrolledCourses, totalCredits } = storeToRefs(store)

const profile = ref({ name: '', email: '', semester: '' })
</script>

<template>
  <section aria-labelledby="profile-heading">
    <h2 id="profile-heading">Student Profile</h2>
    <form @submit.prevent>
      <label for="name">Name</label>
      <input id="name" v-model="profile.name" />
      <label for="email">Email</label>
      <input id="email" type="email" v-model="profile.email" />
      <label for="semester">Semester</label>
      <input id="semester" type="number" v-model="profile.semester" />
    </form>
  </section>

  <section aria-labelledby="enrolled-heading">
    <h2 id="enrolled-heading">Enrolled Courses ({{ enrolledCourses.length }})</h2>
    <p>Total credits: {{ totalCredits }}</p>
    <ul>
      <li v-for="c in enrolledCourses" :key="c.id">
        {{ c.name }} ({{ c.code }})
        <button @click="store.unenroll(c.id)">Remove</button>
      </li>
    </ul>
  </section>
</template>
