<template>
  <div>
    <ProjectChat v-for="item in list" :key="item.nombre"/>
  </div>
</template>
<script>

import ProjectChat from './Chat'

export default {
  name: "ProjectChats",
  components: {
    ProjectChat
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