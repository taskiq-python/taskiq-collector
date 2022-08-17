<template>
  <section>
    <b-tabs position="is-centered" class="block">
      <b-tab-item label="Task info">
        <div>Task id: {{ task.task_id }}</div>
        <div>Task name: {{ task.task_name }}</div>
        <div>Execution time: {{ task.execution_time }}</div>
        <div>Completed: {{ task.completed }}</div>
        <div>
          Positional arguments:
          <pre>{{ task.args }}</pre>
        </div>
        <div>
          Keyword arguments:
          <pre>{{ task.kwargs }}</pre>
        </div>

        <div>
          Return value:
          <pre>{{ task.return_value }}</pre>
        </div>
      </b-tab-item>
      <b-tab-item label="labels">
        <pre>{{ JSON.stringify(task.labels, null, 2) }}</pre>
      </b-tab-item>
      <b-tab-item label="Logs" :disabled="task.log === ''">
        <pre>{{ task.log }}</pre>
      </b-tab-item>
    </b-tabs>
  </section>
</template>

<script>
export default {
  props: {
    task: {
      type: Object,
      default: () => {},
    },
  },
}
</script>

<style scoped>
.log {
  border: 2px;
  border-color: aquamarine;
  border-radius: 20;
}
</style>
