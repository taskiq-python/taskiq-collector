import TaskService from '~/services/task_service'

export default ({ $axios }, inject) => {
  inject('taskService', new TaskService($axios))
}
