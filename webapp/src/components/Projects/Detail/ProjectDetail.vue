<template>
  <div class="p-4 pr-4 mr-1" style="overflow: auto; height:90vh;">

    <div class="columns btn-back" @click="backToMain">
        <span class="column is-1 material-icons-round" style="color:#757575">arrow_back</span>
        <p class="column" style="color:#757575; margin-left:-15px"> Back </p>
    </div>
    
    <div style="margin-top:-20px" class="mb-5">
      <b class="is-size-4" style="color: #181818"> {{this.project.name}} </b>
    </div>
    
    <div class="mt-4" v-if="this.project.description">
        <b>Description</b>
    </div>
    <p v-if="this.project.description">{{ this.project.description }}</p>

    <div class="mt-4 columns">
        <div class="column">
            <b>Start date</b>
            <p>{{ this.project.start_date }}</p>
        </div>
        <div class="column" v-if="this.project.end_date">
            <b>End date</b>
            <p>{{ this.project.end_date }}</p>
        </div>
    </div>
    <div class="mt-4 tabs">
        <ul>
            <li v-bind:class="{'is-active' : this.type == 'tasks'}" @click="type = 'tasks'"><a>Tasks</a></li>
            <li v-bind:class="{'is-active' : this.type == 'files'}" @click="type = 'files'"><a>Files</a></li>
            <li v-bind:class="{'is-active' : this.type == 'chat'}" @click="type = 'chat'"><a>Messages</a></li>
        </ul>
    </div>
    <ProjectTasks v-bind:project="this.project" v-if="type == 'tasks'"/>
    <ProjectChats v-if="type == 'chat'"/>
  </div>
</template>

<script>
import ProjectTasks from './Tasks'
import ProjectChats from './Chat/Chats'

export default {
  name: 'ProjectDetail',
  components: {
    ProjectTasks,
    ProjectChats
  },
  props: ['project'],
  data () {
    return {
      type: 'tasks',
      tasks: []
    }
  },
  methods: {
    backToMain () {
      this.$store.commit('setCurrentScreen', { screen: 'main' })
    },
    addNewTask () {
      this.tasks.push({
        nombre: '',
        responsable: '',
        descripcion: ''
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.btn-back {
  cursor: pointer;
}

.collapse-focus:focus {
  outline: none;
  box-shadow: none;
}

::-webkit-scrollbar {
  width: 8px;               /* width of the entire scrollbar */
}

::-webkit-scrollbar-track {
  background: transparent;        /* color of the tracking area */
}

::-webkit-scrollbar-thumb {
  background-color: $primary;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid transparent;  /* creates padding around scroll thumb */
}
</style>
