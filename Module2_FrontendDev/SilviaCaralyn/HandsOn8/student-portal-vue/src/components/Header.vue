<script setup>
import { useEnrollmentStore } from '../stores/enrollment.js'

const store = useEnrollmentStore()
</script>

<template>
  <header>
    <span>Student Portal</span>
    <nav aria-label="Main navigation">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>
    <span>Enrolled: {{ store.enrolledCourses.length }}</span>
  </header>
</template>
