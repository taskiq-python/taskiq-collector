<template>
  <section class="section">
    <TaskTable
      :initial-search-params="searchParams"
      @searchUpdated="updateQuery"
      @selectedTask="selectTask"
    ></TaskTable>
  </section>
</template>

<script>
import TaskTable from '~/components/TaskTable.vue'

export default {
  name: 'TasksList',
  components: {
    TaskTable,
  },
  data() {
    return {
      searchParams: {},
    }
  },
  created() {
    this.searchParams = this.$route.query
  },
  methods: {
    async updateQuery(searchParams) {
      for (const key in searchParams) {
        if (searchParams[key] === null) {
          delete searchParams[key]
        }
      }
      await this.$router.push({
        path: 'tasks',
        query: searchParams,
      })
    },
    async selectTask(selected) {
      await this.$router.push(`/tasks/${selected.task_id}`)
    },
  },
}
</script>
