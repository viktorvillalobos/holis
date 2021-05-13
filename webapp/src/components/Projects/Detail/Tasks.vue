<template>
  <div>
    <div class="main-loader">
      <div :class="{'card' : true, 'loader-wrapper' : true, 'is-active' : loading}">
        <div class="card-content">
          <div class="loader is-loading"></div>
        </div>
      </div>
    </div>
    <draggable v-model="tasks" :move="checkMove">
        <transition-group>
            <div class="columns" v-for="(task, index) in tasks" :key="task.uuid">
                <div class="column is-1 check-absolute">
                    <input type="checkbox" v-model="task.is_done" @change="updateCheck(index)">
                </div>
                <Collapsible class="column">
                    <div slot="trigger" class="collapse-focus">
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

                    <div slot="closedTrigger" class="collapse-focus">
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
                            <b style="is-size-6">Nombre</b>
                            <input v-if="task.titleEdit" v-model="task.title" class="input" type="text" placeholder="Ej: Hexagonal interactivo" @blur="task.titleEdit = false; $emit('update')"
                @keyup.enter="updateTitle(index); $emit('update')">
                            <p v-else @click="task.titleEdit=true">{{ task.title }}</p>
                        </div>
                        <div class="column">
                            <div>
                                <b style="is-size-6">Responsable</b>
                            </div>
                            <div :class="{'dropdown' : true, 'is-active' : task.dropdownActive}"> <!-- task -->
                                <div class="dropdown-trigger">
                                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu" @click="task.dropdownActive = true">
                                    <span v-if="task.assigned_to">{{ task.assigned_to.name }}</span>
                                    <span v-else>Seleccionar</span>
                                    <span class="icon is-small">
                                        <i class="fas fa-angle-down" aria-hidden="true"></i>
                                    </span>
                                    </button>
                                </div>
                                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                                    <div class="dropdown-content">
                                        <a @click="selectUser(user, index)" :class="{'dropdown-item' : true, 'is-active' : (user.id == task.assigned_to.id && task.dropdownActive)}" v-for="user in users" :key="user.id">
                                            {{ user.name }}
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-2">
                        <p style="is-size-6"><b>Descripción</b> (opcional)</p>
                        <textarea v-if="task.contentEdit" v-model="task.content" class="textarea" placeholder="e.g. Hello world" @blur="task.contentEdit = false; $emit('update')"
                @keyup.enter="updateContent(index); $emit('update')"></textarea>
                        <p v-else @click="task.contentEdit=true">{{ task.content }}</p>
                    </div>
                    <div class="mt-2" align="right">
                        <button @click="deleteTask(index)" class="button is-danger is-inverted is-small">Borrar</button>
                        <!--<button @click="duplicateTask(task)" class="button is-primary is-inverted is-small">Duplicar</button>-->
                    </div>
                </Collapsible>
            </div>
        </transition-group>
    </draggable>

    <div class="mt-6" align="right">
        <button @click="modalNewTask = true" class="button is-primary is-inverted is-small">Agregar tarea nueva</button>
    </div>

    <div class="modal" :class="{'is-active' : modalNewTask}">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
            <p class="modal-card-title">Crear tarea</p>
            <button class="delete" aria-label="close" @click="modalNewTask = false"></button>
            </header>
            <section class="modal-card-body">
                <div class="mt-2 columns">
                    <div class="column">
                        <b style="is-size-6">Nombre</b>
                        <input v-model="newTask.title" class="input" type="text" placeholder="Ej: Hexagonal interactivo">
                    </div>
                    <div class="column">
                        <div>
                            <b style="is-size-6">Responsable</b>
                        </div>
                        <div :class="{'dropdown' : true, 'is-active' : newTask.dropdownActive}"> <!-- task -->
                            <div class="dropdown-trigger">
                                <button class="button" aria-haspopup="true" aria-controls="dropdown-menu" @click="newTask.dropdownActive = true">
                                <span v-if="newTask.assigned_to">{{ newTask.memberName }}</span>
                                <span v-else>Seleccionar</span>
                                <span class="icon is-small">
                                    <i class="fas fa-angle-down" aria-hidden="true"></i>
                                </span>
                                </button>
                            </div>
                            <div class="dropdown-menu" id="dropdown-menu" role="menu">
                                <div class="dropdown-content">
                                    <a @click="selectUserNewTask(user, index)" :class="{'dropdown-item' : true, 'is-active' : (user.id == newTask.assigned_to && newTask.dropdownActive)}" v-for="user in users" :key="user.id">
                                        {{ user.name }}
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-2">
                    <p style="is-size-6"><b>Descripción</b> (opcional)</p>
                    <textarea v-model="newTask.content" class="textarea" placeholder="e.g. Hello world"></textarea>
                </div>
            </section>
            <footer class="modal-card-foot">
            <button class="button is-success" @click="addNewTask">Crear</button>
            <button class="button" @click="modalNewTask = false">Cancelar</button>
            </footer>
        </div>
    </div>
  </div>
</template>

<script>
import 'vue-collapsible-component/lib/vue-collapsible.css';
import Collapsible from 'vue-collapsible-component';
import { mapState } from 'vuex'
import Draggable from 'vuedraggable'

export default {
  name: "ProjectTasks",
  components: {
      Draggable,
      Collapsible
  },
  props:["project"],
  computed: {
    ...mapState({
      tasksState: state => state.projects.tasks,
      users: state => state.chat.users
    })
  },
  data(){
    return {
        tasks: [],
        modalNewTask: false,
        loading:true,
        newTask: {
            "title": "Ejemplo Tarea",
            "content": "",
            "assigned_to": null,
            "dropdownActive": false
        }
    }
  },
  created(){
    this.$store.dispatch('getUsers')
    this.getTasks()
  },
  methods:{
    checkMove(evt){
        const futureIndex = evt.draggedContext.futureIndex
        const index = evt.draggedContext.index
        const task = this.tasks[index]
        const data = {
            "project_uuid": this.project.uuid,
            "task": task.uuid,
            "index": futureIndex
        }
        this.$store.dispatch('moveTask', data)
    },
    getTasks(){
        this.$store.dispatch('getTasksProject', this.project.uuid)
    },
    deleteTask(index){
        const payload = {
            'task':this.tasks[index].uuid,
            'project_uuid': this.project.uuid
        }
        this.$store.dispatch('deleteTask', payload)
        this.loading = true
    },
    addNewTask(){
        const tasks = []
        tasks.push(this.newTask)
        const payload = {
            'tasks':tasks,
            'project_uuid': this.project.uuid
        }
        this.$store.dispatch('addTaskProject', payload)
        this.modalNewTask = false
        this.loading = true
    },
    selectUserNewTask(user){
        this.newTask.assigned_to = user.id
        this.newTask.memberName = user.name
        this.newTask.dropdownActive = false
    },
    selectUser(user, index){
        this.tasks[index].assigned_to.id = user.id
        this.tasks[index].assigned_to.name = user.name
        this.tasks[index].dropdownActive = false
        this.updateAssigned(index)
    },
    updateAssigned(index){
        const payload = {
            'uuid' : this.project.uuid,
            'task' : this.tasks[index].uuid,
            'data' : {
                'assigned_to_id' :  this.tasks[index].assigned_to.id
            }
        }
        this.$store.dispatch('updateTask', payload)
    },
    updateCheck(index){
        const payload = {
            'uuid' : this.project.uuid,
            'task' : this.tasks[index].uuid,
            'data' : {
                'is_done' : this.tasks[index].is_done
            }
        }
        this.$store.dispatch('updateTask', payload)
    },
    updateTitle(index){
        this.tasks[index].titleEdit = false
        const payload = {
            'uuid' : this.project.uuid,
            'task' : this.tasks[index].uuid,
            'data' : {
                'title' : this.tasks[index].title
            }
        }
        this.$store.dispatch('updateTask', payload)
    },
    updateContent(index){
        this.tasks[index].contentEdit = false
        const payload = {
            'uuid' : this.project.uuid,
            'task' : this.tasks[index].uuid,
            'data' : {
                'content' : this.tasks[index].content
            }
        }
        this.$store.dispatch('updateTask', payload)
    }
  },
  watch: {
      tasksState(tasks){
          console.log(tasks)
          this.loading = false
          this.tasks = JSON.parse(JSON.stringify(tasks)) // Tuve que crear una copia para no modificar la variable mutable directamente
      }
  }
};
</script>

<style lang="scss" scoped>
.collapse-focus:focus {
  outline: none;
  box-shadow: none;
}

.check-absolute{
    margin-top: 10px;
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