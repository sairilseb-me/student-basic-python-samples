<script setup>
import { ref } from 'vue'

const message = ref('Hello, Vue 3!')
const students = ref([])

const getStudents = async () => {
   const response = await fetch('http://localhost:5000/api/students')
   students.value = await response.json()
}

</script>

<template>
  <div>
    <h1>Welcome to the WIT Student Python Examples</h1>
    <p>{{ message }}</p>
    <button @click="getStudents">Get Students</button>
    <ul v-if="students.length > 0">
      <li v-for="student in students" :key="student.id">
        {{ student.name }} - {{ student.status }}
      </li>
    </ul>
  </div>
</template>

<style scoped></style>
