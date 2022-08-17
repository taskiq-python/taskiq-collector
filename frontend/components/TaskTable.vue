<template>
  <div class="container vh-100">
    <b-field grouped group-multiline>
      <b-select
        v-model="searchParams.isErr"
        placeholder="Is error"
        icon="alert-outline"
      >
        <option :value="null"></option>
        <option :value="true">Only with errors</option>
        <option :value="false">Without errors</option>
      </b-select>
      <b-select
        v-model="searchParams.completed"
        placeholder="Completed"
        icon="check-all"
      >
        <option :value="null"></option>
        <option :value="true">Only completed tasks</option>
        <option :value="false">Only not completed tasks</option>
      </b-select>
      <b-select
        v-model="searchParams.limit"
        placeholder="Tasks per page"
        icon="format-list-bulleted"
      >
        <option :value="null"></option>
        <option :value="10">10</option>
        <option :value="20">20</option>
        <option :value="30">30</option>
        <option :value="50">50</option>
        <option :value="100">100</option>
      </b-select>
      <b-input
        v-model="searchParams.taskName"
        placeholder="Task name"
        icon="check-all"
      ></b-input>
      <b-input
        v-model="searchParams.taskId"
        placeholder="Task id"
        icon="check-all"
      ></b-input>
    </b-field>
    <b-table
      :data="tasks_data"
      :loading="isLoading"
      :height="700"
      :row-class="getRowClasses"
      :current-page="currentPage"
      :mobile-cards="true"
      :sticky-header="true"
      :total="totalResults"
    >
      <template #empty>
        <div class="has-text-centered">No records</div>
      </template>

      <b-table-column key="task_id" v-slot="props" label="ID">
        <a @click="selectItem(props.row)">
          {{ props.row.task_id }}
        </a>
      </b-table-column>

      <b-table-column key="task_name" v-slot="props" label="Task name">
        {{ props.row.task_name }}
      </b-table-column>

      <b-table-column key="completed" v-slot="props" label="Completed">
        {{ props.row.completed }}
      </b-table-column>

      <b-table-column key="is_err" v-slot="props" label="Is error">
        {{ props.row.is_err }}
      </b-table-column>
      <b-table-column key="created" v-slot="props" label="Created">
        {{ props.row.created }}
      </b-table-column>
    </b-table>
    <div>
      <b-button @click="goBackward">&lt;</b-button>
      <b-button @click="goForward">&gt;</b-button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    initialSearchParams: {
      type: Object,
      default() {
        return {
          isErr: null,
          completed: null,
          forward: true,
          cursor: null,
        }
      },
    },
  },
  data() {
    return {
      interval: undefined,
      isLoading: false,
      tasks_data: [],
      totalResults: 0,
      currentPage: 1,
      searchParams: {},
      hasNext: true,
    }
  },
  watch: {
    searchParams: {
      async handler(newSearchParams) {
        await this.updateTasks()
        if (this.searchParams !== this.initialSearchParams) {
          this.$emit('searchUpdated', this.searchParams)
        }
      },
      deep: true,
    },
  },
  beforeDestroy() {
    if (this.interval) {
      clearInterval(this.interval)
      this.interval = undefined
    }
  },
  async mounted() {
    this.searchParams = Object.assign({}, this.initialSearchParams)
    await this.updateTasks()
    this.interval = setInterval(this.updateTasks, 3000)
  },
  methods: {
    async updateTasks() {
      const resp = await this.$taskService.get_tasks(this.searchParams)
      if (resp.status !== 200) {
        return
      }
      this.tasks_data = resp.data.results.sort(
        (left, right) => right.id - left.id
      )
      this.hasNext = resp.data.has_next
      if (this.isLoading) {
        this.isLoading = false
      }
    },
    getRowClasses(row, index) {
      if (row.is_err) {
        return 'error-task'
      }
    },
    selectItem(newSelected) {
      this.$emit('selectedTask', newSelected)
    },
    goForward() {
      let itemId = null
      if (this.tasks_data.length > 0) {
        itemId = this.tasks_data.sort((left, right) => left.id - right.id)[0].id
      } else {
        itemId = this.searchParams.afterId + 1
      }
      this.searchParams.beforeId = itemId
      this.searchParams.afterId = null
      this.isLoading = true
      this.$emit('searchUpdated', this.searchParams)
    },
    goBackward() {
      let itemId = null
      if (this.tasks_data.length > 0) {
        itemId = this.tasks_data.sort((left, right) => right.id - left.id)[0].id
      } else {
        itemId = this.searchParams.beforeId - 1
      }
      this.searchParams.afterId = itemId
      this.searchParams.beforeId = null
      this.isLoading = true
      this.$emit('searchUpdated', this.searchParams)
    },
  },
}
</script>

<style>
tr.error-task {
  background: #fdc9c9;
  color: #000;
}

vh-100 {
  height: 100vh;
}
</style>
