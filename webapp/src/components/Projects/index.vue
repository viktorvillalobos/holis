<template>
  <div class="p-4 pr-4">
    <Projects ref="Projects" v-if="this.currentScreen.screen == 'main'"/>
    <CreateProject v-bind:typeProject="this.currentScreen.data" v-if="this.currentScreen.screen == 'create'"/>
    <DetailProject v-bind:project="this.currentScreen.data" v-if="this.currentScreen.screen == 'detail'"/>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Card from '@/components/Card'
import Projects from './Projects/Projects'
import CreateProject from './Create/CreateProject'
import DetailProject from './Detail/ProjectDetail'

export default {
  name: 'MainProjects',
  components: {
    Card,
    Projects,
    CreateProject,
    DetailProject
  },
  data () {
    return {
      type: 'my_projects'
    }
  },
  computed: {
    ...mapState({
      currentScreen: state => state.projects.currentScreen
    })
  },
  methods: {
    openCreateProject () {
      // this.$store.commit('setCreateProjectActive')
      // setTimeout(() => {  this.$store.commit('setTypeProject', this.type) }, 2000); // espero un segundo por condicion de carrera que se cree la vista para pasarle el type
    }
  }
}
</script>

<style lang="scss" scoped>
.projects{
  padding: 10px;
  padding-right: 10px;
}
</style>
