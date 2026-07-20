<script setup>
defineProps({
  id: Number,
  name: String,
  code: String,
  credits: Number,
  grade: String,
})

const emit = defineEmits(['enroll'])
</script>

<template>
  <article class="course-card" tabindex="0">
    <h3>{{ name }}</h3>
    <p>{{ code }} — {{ credits }} credits</p>
    <span>Grade: {{ grade }}</span>
    <div>
      <button @click="emit('enroll', { id, name, code, credits, grade })">Enroll</button>
    </div>
  </article>
</template>
