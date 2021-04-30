<template>
  <div>
    <draggable v-model="tasks">
        <transition-group>
            <div v-for="(task, index) in tasks" :key="task">
                {{task}}
                <div class="check-absolute">
                    <input type="checkbox" v-model="task.is_done" @change="updateCheck(index)">
                </div>
                <Collapsible>
                    <div slot="trigger" class="collapse-focus m-3">
                        <div class="customTrigger">
                            <div class="columns">
                                <div class="column ml-5">
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
                                    <p class="mt-2 ml-5 is-size-5">{{ task.title }}</p>
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
                    <!--<div class="mt-2" align="right">
                        <button @click="deleteTask(index)" class="button is-danger is-inverted is-small">Borrar</button>
                        <button @click="duplicateTask(task)" class="button is-primary is-inverted is-small">Duplicar</button>
                    </div>-->
                </Collapsible>
            </div>
        </transition-group>
    </draggable>
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
        tasks: []
    }
  },
  created(){
    this.$store.dispatch('getUsers')
    this.getTasks()
  },
  methods:{
    getTasks(){
        this.$store.dispatch('getTasksProject', this.project.uuid)
    },
    addNewTask(){
        this.tasks.push({
            "nombre" : "",
            "responsable" : "",
            "descripcion" : ""
        })
    },
    selectUser(user, index){
        this.tasks[index].assigned_to.id = user.id
        this.tasks[index].assigned_to.name = user.name
        this.tasks[index].dropdownActive = false
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
        const dataEdit = {
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
    position: absolute;
    margin-top: 22px;

}
</style>