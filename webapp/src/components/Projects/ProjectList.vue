<template>
  <div>
    <div align="right">
      {{type}}
        <div class="select is-small is-primary mr-2">
            <select>
            <option>Todos</option>
            <option>Activos</option>
            <option>Cerrados</option>
            <option>Futuros</option>
            </select>
        </div>
    </div>
    <Project v-for="item in list" :key="item.nombre"/>
  </div>
</template>
<script>
import Project from './Project'
export default {
  name: "ProjectList",
  components: {
    Project
  },
  props: ['type'],
  data(){
      return {
        list: [
            { nombre: "Nombre"},
            { nombre: "Nombre"},
            { nombre: "Nombre"}
        ],
      }
  },
  created(){
      
  },
  methods:{
    getProjects(){
      var type = 1
      switch(this.type) {
        case 'my_projects':
          type = 1
          break;
        case 'my_team':
          type = 2
          break;
        default:
          type = 3
      }
      console.log("Entre aqui")
      try {
          this.$store.dispatch('getProjects', type)
      } catch (e) {
          console.log('couldnt load notifications')
      }
    }
  },
  watch: {
    type: function (newType, oldType) {
        this.getProjects()
    }
  }
};
</script>