<template>
  <div class="projects">
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
  font-family: $family-dm-sans;
}

.scroll-projects{
  overflow: auto;
  margin-right: 5px;
}

.scroll-projects::-webkit-scrollbar {
  width: 8px;               /* width of the entire scrollbar */
}

.scroll-projects::-webkit-scrollbar-track {
  background: transparent;        /* color of the tracking area */
}

.scroll-projects::-webkit-scrollbar-thumb {
  background-color: $primary;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid transparent;  /* creates padding around scroll thumb */
}
</style>
