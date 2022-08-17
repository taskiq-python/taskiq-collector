<template>
  <div>
    <b-navbar>
      <template #start>
        <b-navbar-item tag="router-link" :to="{ name: 'index' }">
          Metrics
        </b-navbar-item>
        <b-navbar-item tag="router-link" :to="{ name: 'tasks' }">
          Tasks list
        </b-navbar-item>
      </template>
    </b-navbar>
    <Nuxt />
  </div>
</template>

<script>
export default {
  name: 'DefaultLayout',
}
</script>
