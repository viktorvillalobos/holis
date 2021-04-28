<template>
  <div>
    <draggable v-model="tasks">
        <transition-group>
            <div v-for="(task, index) in tasks" :key="task">
                <Collapsible>
                    <div slot="trigger" class="collapse-focus m-3">
                        <div class="column is-1">
                            <input type="checkbox">
                        </div>
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
                            <b style="is-size-6">Nombre</b>
                            <input v-if="task.titleEdit" v-model="task.title" class="input" type="text" placeholder="Ej: Hexagonal interactivo" @blur="task.titleEdit = false; $emit('update')"
                @keyup.enter="task.titleEdit=false; $emit('update')">
                            <p v-else @click="task.titleEdit = true">{{ task.title }}</p>
                        </div>
                        <div class="column">
                            <div>
                                <b style="is-size-6">Responsable</b>
                            </div>
                            <div :class="{'dropdown' : true, 'is-active' : task.dropdownActive}"> <!-- task -->
                                <div class="dropdown-trigger">
                                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu" @click="task.dropdownActive = true">
                                    <span v-if="task.member">{{ task.memberName }}</span>
                                    <span v-else>Seleccionar</span>
                                    <span class="icon is-small">
                                        <i class="fas fa-angle-down" aria-hidden="true"></i>
                                    </span>
                                    </button>
                                </div>
                                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                                    <div class="dropdown-content">
                                        <a @click="selectUser(user, index)" :class="{'dropdown-item' : true, 'is-active' : (user.id == task.member && task.dropdownActive)}" v-for="user in users" :key="user.id">
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
                @keyup.enter="task.contentEdit=false; $emit('update')"></textarea>
                        <p v-else @click="task.contentEdit = true">{{ task.content }}</p>
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
      tasks: state => state.projects.tasks
    })
  },
  data(){
    return {}
  },
  created(){
    this.getTasks()
  },
  methods:{
    getTasks(){
        //this.loading = true
        this.$store.dispatch('getTasksProject', this.project.uuid)
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