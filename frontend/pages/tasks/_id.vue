<template>
  <section class="section">
    <TaskView v-if="task !== null" :task="task"></TaskView>
    <div v-else>Task not found.</div>
  </section>
</template>

<script>
import TaskView from '~/components/TaskView.vue'

export default {
  components: { TaskView },
  data() {
    return {
      task: null,
    }
  },
  async mounted() {
    const response = await this.$taskService.get_task(this.$route.params.id)
    if (response.status === 200) {
      this.task = response.data
    }
  },
}
</script>
