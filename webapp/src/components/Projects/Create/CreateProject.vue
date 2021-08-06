<template>
  <div class="create-project scroll-projects p-4">

    <div class="columns btn-back" @click="backToMain">
        <span class="column is-1 material-icons-round" style="color:#757575">arrow_back</span>
        <p class="column" style="color:#757575; margin-left:-15px"> Back </p>
    </div>
    
    <div style="margin-top:-20px" class="mb-5">
      <b class="is-size-4" style="color: #181818"> Create project </b>
    </div>

    <b class="is-size-6">Name</b>
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

    <b v-if="tasks.length > 0" class="is-size-6">
      Tasks
    </b>

    <draggable v-model="tasks" class="mt-4">
        <transition-group>
            <div v-for="(task, index) in tasks" :key="task" class="card p-4 mb-4">
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

    <button @click="addNewTask" class="button is-large is-fullwidth is-primary is-outlined mt-6">
      <span class="icon">
        <span class="material-icons-round">add_circle_outline</span>
      </span>
      <span style="font-size: 16px;">Add task</span>
    </button>

    <div align="right" class="mt-6" >
      <button @click="createProject" class="button is-primary" :class="{'is-loading': loading}">Create project</button>
    </div>

    <div class="modal" :class="{'is-active' : this.modalError}">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title has-text-danger">Alert</p>
                <button class="delete" aria-label="close" @click="modalError = false"></button>
            </header>
            <section class="modal-card-body">
                {{ this.errorAlert }}
            </section>
            <footer class="modal-card-foot">
                <button class="button is-info is-outlined" @click="modalError = false">Ok</button>
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
        this.errorAlert = 'The project name cannot be less than 4 characters.'
        this.modalError = true
        return false
      }
      if (this.dateStart == '') {
        this.errorAlert = 'Date start cannot be empty'
        this.modalError = true
        return false
      }

      let isValid = true
      this.tasks.forEach(element => {
        if (element.title.length < 3) {
          this.errorAlert = 'The task name ' + element.title + ' cannot be less than 3 characters.'
          this.modalError = true
          isValid = false
          throw BreakException
        }
        if (element.content.length < 3 && element.content.length != 0) {
          this.errorAlert = 'The task description  ' + element.content + ' cannot be less than 3 characters.'
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
        end_date: this.dateEnd == '' ? null : this.dateEnd
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
.btn-back {
  cursor: pointer;
}

.btn-task {
  cursor: pointer;
  padding: 8px;
  font-size: 22px;

  &:hover {
    cursor: pointer;
    color: $primary;
  }
}

.scroll-projects{
  position: absolute;
  overflow: auto;
  margin-right: 5px;
  height: 100%;
  width: 99%;
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
