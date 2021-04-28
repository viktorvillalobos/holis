<template>
  <div class="p-4" style="overflow: auto; height:90vh;">

      <div class="columns">
        <button class="button is-white column is-1" @click="backToMain">
            <span class="icon is-small">
                <font-awesome-icon icon="arrow-left"/>
            </span>
        </button>
        <h1 class="column"> Crear Proyecto </h1>
    </div>
    <b style="is-size-6">Hexagonal interactivo</b>
    <div class="mt-4">
        <b>Descripción</b>
    </div>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. </p>
    <div class="mt-4 columns">
        <div class="column">
            <b>Fecha de inicio</b>
            <p>16/07/1991</p>
        </div>
        <div class="column">
            <b>Fecha de fin</b>
            <p>16/07/1991</p>
        </div>
    </div>
    <div class="mt-4 tabs">
        <ul>
            <li v-bind:class="{'is-active' : this.type == 'tasks'}" @click="type = 'tasks'"><a>Tareas</a></li>
            <li v-bind:class="{'is-active' : this.type == 'files'}" @click="type = 'files'"><a>Archivos</a></li>
            <li v-bind:class="{'is-active' : this.type == 'chat'}" @click="type = 'chat'"><a>Mensajes</a></li>
        </ul>
    </div>
    <ProjectTasks v-if="type == 'tasks'"/>
    <ProjectChats v-if="type == 'chat'"/>
  </div>
</template>

<script>
import ProjectTasks from './Tasks'
import ProjectChats from './Chat/Chats'

export default {
  name: "ProjectDetail",
  components: {
      ProjectTasks,
      ProjectChats
  },
  data(){
    return {
        type: 'tasks',
        tasks: []
    }
  },
  methods:{
      backToMain() {
         this.$store.commit('setCurrentScreen', {'screen' : 'main'})
      },
      addNewTask(){
          this.tasks.push({
              "nombre" : "",
              "responsable" : "",
              "descripcion" : ""
          })
      }
  }
};
</script>

<style lang="scss" scoped>
.collapse-focus:focus {
  outline: none;
  box-shadow: none;
}
</style>