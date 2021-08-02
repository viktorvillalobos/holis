<template>
  <div class="create-project scroll-projects p-4">

    <div class="columns">
        <button class="button is-white column is-1" @click="backToMain">
            <span class="icon is-small">
                <font-awesome-icon icon="arrow-left"/>
            </span>
        </button>
        <h1 class="column"> Create project </h1>
    </div>

    <div class="main-loader">
      <div :class="{'card' : true, 'loader-wrapper' : true, 'is-active' : loading}">
        <div class="card-content">
          <div class="loader is-loading"></div>
        </div>
      </div>
    </div>

    <b style="is-size-6">Name</b>
    <input v-model="name" class="input" type="text" placeholder="Project zero">

    <div class="mt-4">
        <p style="is-size-6"><b>Description</b> (optional)</p>
        <textarea v-model="description" class="textarea" placeholder="Hello world this is my first project"></textarea>
    </div>
    <div class="mt-2 columns">
        <div class="column">
            <b style="is-size-6">Start date</b>
            <input v-model="dateStart" class="input" type="date" :min="currentDate()" placeholder="--/--/----">
        </div>
        <div v-if="dateStart" class="column">
            <b style="is-size-6">End date</b>
            <input v-model="dateEnd" class="input" type="date" :min="dateStart" placeholder="--/--/----">
        </div>
    </div>

    <draggable v-model="tasks">
        <transition-group>
            <div v-for="(task, index) in tasks" :key="task">
                <Collapsible>
                    <div slot="trigger" class="collapse-focus m-3">
                        <div class="customTrigger">
                            <div class="columns">
                                <div class="column">
                                    <p class="mt-2 is-size-5">{{ task.title }}</p>
                                </div>
                                <div class="column" align="right">
                                    <font-awesome-icon class="mt-2" icon="chevron-up" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div slot="closedTrigger" class="collapse-focus m-3">
                        <div class="customTrigger">
                            <div class="columns">
                                <div class="column">
                                    <p class="mt-2 is-size-5">{{ task.title }}</p>
                                </div>
                                <div class="column" align="right">
                                    <font-awesome-icon class="mt-2" icon="chevron-down" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-2 columns">
                        <div class="column">
                            <b style="is-size-6">Name task</b>
                            <input v-model="task.title" class="input" type="text" placeholder="Ej: Hexagonal interactivo">
                        </div>
                        <div class="column">
                            <div>
                                <b style="is-size-6">Responsible</b>
                            </div>
                            <div :class="{'dropdown' : true, 'is-active' : task.dropdownActive}"> <!-- task -->
                                <div class="dropdown-trigger">
                                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu" @click="task.dropdownActive = true">
                                    <span v-if="task.assigned_to">{{ task.memberName }}</span>
                                    <span v-else>Select</span>
                                    <span class="icon is-small">
                                        <i class="fas fa-angle-down" aria-hidden="true"></i>
                                    </span>
                                    </button>
                                </div>
                                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                                    <div class="dropdown-content">
                                        <a @click="selectUser(user, index)" :class="{'dropdown-item' : true, 'is-active' : (user.id == task.assigned_to && task.dropdownActive)}" v-for="user in users" :key="user.id">
                                            {{ user.name }}
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-2">
                        <p style="is-size-6"><b>Description</b> (optional)</p>
                        <textarea v-model="task.content" class="textarea" placeholder="e.g. Hello world"></textarea>
                    </div>
                    <div class="mt-2" align="right">
                      <span @click="duplicateTask(task)" class="material-icons-outlined btn-task">content_copy</span>
                      <span @click="deleteTask(index)" class="material-icons-round btn-task">delete</span>
                    </div>
                </Collapsible>
            </div>
        </transition-group>
    </draggable>

    <div class="mt-6" align="right">
        <button @click="addNewTask" class="button is-primary is-inverted is-small">Add task</button>
    </div>

    <div align=right>
      <button @click="createProject" class="button is-primary">Create project</button>
    </div>

    <div class="modal" :class="{'is-active' : this.modalError}">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title has-text-danger">Alerta</p>
                <button class="delete" aria-label="close" @click="modalError = false"></button>
            </header>
            <section class="modal-card-body">
                {{ this.errorAlert }}
            </section>
            <footer class="modal-card-foot">
                <button class="button is-info is-outlined" @click="modalError = false">Aceptar</button>
            </footer>
        </div>
        <button class="modal-close is-large" aria-label="close" @click="modalError = false"></button>
    </div>
  </div>
</template>

<script>
import 'vue-collapsible-component/lib/vue-collapsible.css'
import Collapsible from 'vue-collapsible-component'
import { mapState } from 'vuex'
import Draggable from 'vuedraggable'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

export default {
  name: 'CreateProject',
  components: {
    Collapsible,
    Draggable
  },
  props: ['typeProject'],
  data () {
    return {
      tasks: [{
        title: 'Example task',
        content: '',
        assigned_to: null,
        dropdownActive: false
      }],
      name: '',
      description: '',
      dateStart: '',
      dateEnd: '',
      loading: false,
      modalError: false,
      errorAlert: ''
    }
  },
  computed: {
    ...mapState({
      project: state => state.projects.project,
      users: state => state.chat.users
    })
  },
  created () {
    this.$store.dispatch('getUsers')
  },
  methods: {
    isValid () {
      if (this.name.length < 3) {
        this.errorAlert = 'El nombre no puede ser menor de 3 caracteres'
        this.modalError = true
        return false
      }
      if (this.dateStart == '') {
        this.errorAlert = 'No debes dejar los campos de fecha vacios'
        this.modalError = true
        return false
      }

      let isValid = true
      this.tasks.forEach(element => {
        if (element.title.length < 3) {
          this.errorAlert = 'El nombre de la tarea ' + element.title + ' no puede ser menor a 3 caracteres'
          this.modalError = true
          isValid = false
          throw BreakException
        }
        if (element.content.length < 3) {
          this.errorAlert = 'La descripcion de la tarea ' + element.content + ' no puede ser menor menor a 3 caracteres '
          this.modalError = true
          isValid = false
          throw BreakException
        }
      })
      return isValid
    },
    selectUser (user, index) {
      this.tasks[index].assigned_to = user.id
      this.tasks[index].memberName = user.name
      this.tasks[index].dropdownActive = false
    },
    backToMain () {
      this.$store.commit('setCurrentScreen', { screen: 'main' })
    },
    createProject () {
      const data = {
        name: this.name,
        description: this.description,
        start_date: this.dateStart,
        end_date: this.dateEnd
      }
      const dataSend = {
        typeProject: this.typeProject,
        data: data,
        tasks: this.tasks
      }
      console.log(data)
      console.log(dataSend)
      if (this.isValid()) {
        this.loading = true
        this.$store.dispatch('createProject', dataSend)
      }
    },
    addNewTask () {
      this.tasks.push({
        title: 'Example task',
        content: '',
        assigned_to: null,
        dropdownActive: false
      })
    },
    duplicateTask (task) {
      this.tasks.push({
        title: task.title,
        content: task.description,
        member: task.assigned_to,
        dropdownActive: task.dropdownActive
      })
    },
    deleteTask (index) {
      this.tasks.splice(index, 1)
    },
    currentDate() {
      const current = new Date();
      const date = `${current.getDay()}/${current.getMonth()+1}/${current.getFullYear()}`;
      return date;
    }
  },
  watch: {
    dateStart: function(newVal){
      this.dateEnd = ''
    },
    project: function (newVal) {
      setTimeout(() => {
        this.loading = false
        this.$store.commit('setCurrentScreen', { screen: 'main' })
      }, 2000)
      console.log('Mogeko', newVal)
    },
    tasks: function (newVal, oldVal) {
      console.log('newVal', newVal)
      console.log('oldVal', oldVal)
    },
    users: function (users) {
      console.log('users', users)
    }
  }
}
</script>

<style lang="scss" scoped>

.btn-task {
  cursor: pointer;
  padding: 8px;
  font-size: 22px;

  &:hover {
    cursor: pointer;
    color: $primary;
  }
}

.create-project{
  font-family: $family-dm-sans;
  height:90vh;
}

.collapse-focus:focus {
  outline: none;
  box-shadow: none;
}
.main-loader{
  width:100%;
}
.loader-wrapper {
  position: absolute;
  left: 35%;
  height: 100;
  width: 100;
  background: #fff;
  opacity: 0;
  z-index: -1;
  transition: opacity .3s;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 6px;

  .loader {
      height: 80px;
      width: 80px;
  }

  &.is-active {
      opacity: 1;
      z-index: 1;
  }
}
</style>
