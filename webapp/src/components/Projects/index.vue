<template>
  <div class="p-4 pr-4">
    <div class="tabs">
      <ul>
          <li v-bind:class="{'is-active' : this.type == 'my_projects'}" @click="type = 'my_projects'"><a>Mis proyectos</a></li>
          <li v-bind:class="{'is-active' : this.type == 'my_team'}" @click="type = 'my_team'"><a>Mi equipo</a></li>
          <li v-bind:class="{'is-active' : this.type == 'my_company'}" @click="type = 'my_company'"><a>Mi empresa</a></li>
      </ul>
    </div>
    <div style="overflow: auto; height:70vh;">
      <ProjectList v-bind:type="this.type"/>
    </div>
    <div align=right>
      <button @click="openCreatProject" class="button is-primary">Crear nuevo proyecto</button>
    </div>
  </div>
</template>

<script>
import Card from "@/components/Card";
import ProjectList from './ProjectList'

export default {
  name: "Projects",
  components: {
    Card,
    ProjectList
  },
  data(){
    return {
      type: "my_projects"
    }
  },
  methods: {
    openCreatProject () {
      this.$store.commit('setCreateProjectActive')
      setTimeout(() => {  this.$store.commit('setTypeProject', this.type) }, 1000); // espero un segundo por condicion de carrera que se cree la vista para pasarle el type
    }
  }
};
</script>

<style lang="scss" scoped>
.projects{
  padding: 10px;
  padding-right: 10px;
}
</style>