<template>
  <div class="p-4" style="overflow: auto; height:90vh;">
    
    <div align="center" :class="{'loader-wrapper' : true, 'is-active' : loading}">
        <div class="loader is-loading"></div>
    </div>
    <b style="is-size-6">Nombre</b>
    <input v-model="name" class="input" type="text" placeholder="Ej: Proyecto ejemplo">

    <div class="mt-2">
        <p style="is-size-6"><b>Descripción</b> (opcional)</p>
        <textarea v-model="description" class="textarea" placeholder="e.g. Hello world"></textarea>
    </div>
    <div class="mt-2 columns">
        <div class="column">
            <b style="is-size-6">Fecha de inicio</b>
            <input v-model="dateStart" class="input" type="date" placeholder="--/--/----">
        </div>
        <div class="column">
            <b style="is-size-6">Fecha de término</b>
            <input v-model="dateEnd" class="input" type="date" placeholder="--/--/----">
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
                            <b style="is-size-6">Nombre</b>
                            <input v-model="task.title" class="input" type="text" placeholder="Ej: Hexagonal interactivo">
                        </div>
                        <div class="column">
                            <div>
                                <b style="is-size-6">Responsable</b>
                            </div>
                            <div class="dropdown"> <!-- task -->
                                <div class="dropdown-trigger">
                                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
                                    <span>Todos</span>
                                    <span class="icon is-small">
                                        <i class="fas fa-angle-down" aria-hidden="true"></i>
                                    </span>
                                    </button>
                                </div>
                                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                                    <div class="dropdown-content">
                                    <a href="#" class="dropdown-item is-active">
                                        Todos
                                    </a>
                                    <a class="dropdown-item">
                                        Activos
                                    </a>
                                    <a href="#" class="dropdown-item">
                                        Cerrados
                                    </a>
                                    <a href="#" class="dropdown-item">
                                        Futuros
                                    </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-2">
                        <p style="is-size-6"><b>Descripción</b> (opcional)</p>
                        <textarea v-model="task.content" class="textarea" placeholder="e.g. Hello world"></textarea>
                    </div>
                    <div class="mt-2" align="right">
                        <button @click="deleteTask(index)" class="button is-danger is-inverted is-small">Borrar</button>
                        <button @click="addNewTask" class="button is-primary is-inverted is-small">Duplicar</button>
                    </div>
                </Collapsible>
            </div>
        </transition-group>
    </draggable>

    <div class="mt-6" align="right">
        <button @click="addNewTask" class="button is-primary is-inverted is-small">Agregar tarea nueva</button>
    </div>

    <div align=right>
      <button @click="createProject" class="button is-primary">Crear proyecto</button>
    </div>
  </div>
</template>

<script>
import 'vue-collapsible-component/lib/vue-collapsible.css';
import Collapsible from 'vue-collapsible-component';
import { mapState } from 'vuex'
import Draggable from 'vuedraggable'

export default {
  name: "CreateProject",
  components: {
      Collapsible,
      Draggable
  },
  data(){
    return {
        tasks: [],
        name: '',
        description: '',
        dateStart: '',
        dateEnd: '',
        loading: false
    }
  },
  computed: {
    ...mapState({
        typeProject: state => state.projects.typeProject,
        project: state => state.projects.project
    })
  },
  methods:{
      createProject(){
          const data = {
              'name': this.name,
              'description': this.description,
              'start_date': this.dateStart,
              'end_date': this.dateEnd,
              'company_id': 1
          }
          const dataSend = {'typeProject' : this.typeProject, 
                            'data' : data,
                            'tasks':this.tasks}
          this.loading = true
          this.$store.dispatch('createProject', dataSend)
      },
      addNewTask(){
          this.tasks.push({
              "title" : "Ejemplo Tarea",
              "content" : ""
          })
      },
      deleteTask(index){
        this.tasks.splice(index,1)
      }
  },
  watch:{
    project: function(newVal){
        setTimeout(() => {  this.loading = false }, 2000);
        console.log("Mogeko",newVal)
    },
    tasks: function(newVal,oldVal){
        console.log("newVal",newVal)
        console.log("oldVal",oldVal)
    }
  }
};
</script>

<style lang="scss" scoped>
.collapse-focus:focus {
  outline: none;
  box-shadow: none;
}
.loader-wrapper {
  position: absolute;
margin-left: auto;
margin-right: auto;
left: 0;
right: 0;
text-align: center;
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