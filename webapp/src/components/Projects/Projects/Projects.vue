<template>
  <div class="is-flex is-flex-direction-column">
    <div class="is-flex-grow-1 ml-4 mr-4 mt-3">
      <div class="tabs">
        <ul>
          <li v-bind:class="{'is-active' : this.type == 'my_projects'}" @click="type = 'my_projects'"><a>Mis proyectos</a></li>
          <li v-bind:class="{'is-active' : this.type == 'my_team'}" @click="type = 'my_team'"><a>Mi equipo</a></li>
          <li v-bind:class="{'is-active' : this.type == 'my_company'}" @click="type = 'my_company'"><a>Mi empresa</a></li>
        </ul>
      </div>
    </div>
    <div>
      <div align=right v-if="this.type != 'my_company'" class="is-flex-grow-1 mr-5 mt-5">
        <button @click="openCreateProject" class="button is-primary">New Project</button>
      </div>
    </div>
    <div class="scroll-projects pr-4 pt-4">
        <ProjectList v-bind:type="this.type"/>
    </div>
  </div>
</template>

<script>
import Card from '@/components/Card'
import ProjectList from './ProjectList'

export default {
  name: 'Projects',
  components: {
    Card,
    ProjectList
  },
  data () {
    return {
      type: 'my_projects'
    }
  },
  methods: {
    openCreateProject () {
      this.$store.commit('setCurrentScreen', { screen: 'create', data: this.type })
    }
  }
}
</script>

<style lang="scss" scoped>
.projects{
  padding: 10px;
  padding-right: 10px;
}

.scroll-projects{
  position: absolute;
  overflow: auto;
  margin-right: 5px;
  height: 82%;
  width: 99%;
  top: 18%;
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
