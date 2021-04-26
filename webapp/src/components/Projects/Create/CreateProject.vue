<template>
  <div style="overflow: auto; height:90vh;">

    <div class="columns">
        <button class="button is-white column is-1" @click="backToMain">
            <span class="icon is-small">
                <font-awesome-icon icon="arrow-left"/>
            </span>
        </button>
        <h1 class="column"> Crear Proyecto </h1>
    </div>

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
                        <textarea v-model="task.content" class="textarea" placeholder="e.g. Hello world"></textarea>
                    </div>
                    <div class="mt-2" align="right">
                        <button @click="deleteTask(index)" class="button is-danger is-inverted is-small">Borrar</button>
                        <button @click="duplicateTask(task)" class="button is-primary is-inverted is-small">Duplicar</button>
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
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

export default {
  name: "CreateProject",
  components: {
      Collapsible,
      Draggable
  },
  props: ['typeProject'],
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
        project: state => state.projects.project,
        users: state => state.chat.users
    })
  },
  created(){
      this.$store.dispatch('getUsers')
  },
  methods:{
      selectUser(user, index){
        this.tasks[index].member = user.id
        this.tasks[index].memberName = user.name
        this.tasks[index].dropdownActive = false
      },
      backToMain() {
         this.$store.commit('setCurrentScreen', 'main')
      },
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
        console.log(data)
        console.log(dataSend)
        this.loading = true
        this.$store.dispatch('createProject', dataSend)
      },
      addNewTask(){
        this.tasks.push({
            "title": "Ejemplo Tarea",
            "content": "",
            "member": null,
            "dropdownActive": false
        })
      },
      duplicateTask(task){
          this.tasks.push({
            "title": task.title,
            "content": task.description,
            "member": task.member,
            "dropdownActive": task.dropdownActive
        })
      },
      deleteTask(index){
        this.tasks.splice(index,1)
      }
  },
  watch:{
    project: function(newVal){
        setTimeout(() => {  
            this.loading = false 
            this.$store.commit('setCurrentScreen', 'main')
        }, 2000);
        console.log("Mogeko",newVal)
    },
    tasks: function(newVal,oldVal){
        console.log("newVal",newVal)
        console.log("oldVal",oldVal)
    },
    users: function(users){
        console.log("users",users)
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