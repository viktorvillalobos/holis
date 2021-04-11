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
  watch: {
    type: function (newType, oldType) {
        
    }
  }
};
</script>