<template>
  <div>
    <div align="right">
        <div class="select is-small is-primary mr-2">
            <select>
            <option>Todos</option>
            <option>Activos</option>
            <option>Cerrados</option>
            <option>Futuros</option>
            </select>
        </div>
    </div>
    <Loading v-bind:loading="loading"/>
    <Project v-bind:project="project" v-for="project in projects" :key="project.id"/>
  </div>
</template>
<script>
import Project from './Project'
import Loading from '../../Loading'
import { mapState } from 'vuex'

export default {
  name: 'ProjectList',
  components: {
    Project,
    Loading
  },
  props: ['type'],
  data () {
    return {
      loading: false
    }
  },
  created () {
    this.getProjects()
  },
  computed: {
    ...mapState({
      projects: state => state.projects.projects
    })
  },
  methods: {
    getProjects () {
      this.loading = true
      this.$store.dispatch('getProjects', this.type)
    }
  },
  watch: {
    type: function (newType, oldType) {
      this.getProjects()
    },
    projects: function (newType) {
      console.log('TUNDIII', newType)
      this.loading = false
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
