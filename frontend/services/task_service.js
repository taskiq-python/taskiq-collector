export default class TaskService {
  /**
   * Retuns new task service.
   * @param {import("axios/index").AxiosStatic} axios
   */
  constructor(axios) {
    this.axios = axios
  }

  async get_tasks({
    isErr,
    taskId,
    completed,
    taskName,
    limit,
    beforeId,
    afterId,
  }) {
    const resp = await this.axios.get('/api/tasks', {
      params: {
        limit,
        completed,
        before_id: beforeId,
        after_id: afterId,
        task_name: taskName,
        task_id: taskId,
        is_err: isErr,
      },
    })
    return resp
  }

  async get_task(taskId) {
    return await this.axios.get(`/api/tasks/${taskId}`)
  }

  async delete_task(taskId) {
    return await this.axios.delete(`/api/tasks/${taskId}`)
  }
}
