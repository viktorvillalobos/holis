<template>
  <div class="p-4" style="overflow: auto; height:90vh;">
    <b style="is-size-6">Nombre</b>
    <input class="input" type="text" placeholder="Ej: Proyecto ejemplo">

    <div class="mt-2">
        <p style="is-size-6"><b>Descripción</b> (opcional)</p>
        <textarea class="textarea" placeholder="e.g. Hello world"></textarea>
    </div>
    <div class="mt-2 columns">
        <div class="column">
            <b style="is-size-6">Fecha de inicio</b>
            <input class="input" type="date" placeholder="--/--/----">
        </div>
        <div class="column">
            <b style="is-size-6">Fecha de término</b>
            <input class="input" type="date" placeholder="--/--/----">
        </div>
    </div>
    
    <div v-for="task in this.tasks" :key="task">
        <Collapsible>
            <div slot="trigger" class="collapse-focus m-3">
                <div class="customTrigger">
                    <div class="columns">
                        <div class="column">
                            <p class="mt-2 is-size-5">Hexagonal interactivo</p>
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
                            <p class="mt-2 is-size-5">Hexagonal interactivo</p>
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
                    <input class="input" type="text" placeholder="Ej: Hexagonal interactivo">
                </div>
                <div class="column">
                    <div>
                        <b style="is-size-6">Responsable</b>
                    </div>
                    <div class="dropdown is-active">
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
                <textarea class="textarea" placeholder="e.g. Hello world"></textarea>
            </div>
            <div class="mt-2" align="right">
                <button @click="addNewTask" class="button is-danger is-inverted is-small">Borrar</button>
                <button @click="addNewTask" class="button is-primary is-inverted is-small">Duplicar</button>
            </div>
        </Collapsible>
    </div>

    <div class="mt-6" align="right">
        <button @click="addNewTask" class="button is-primary is-inverted is-small">Agregar tarea nueva</button>
    </div>
  </div>
</template>

<script>
import 'vue-collapsible-component/lib/vue-collapsible.css';
import Collapsible from 'vue-collapsible-component';

export default {
  name: "CreateProject",
  components: {
      Collapsible
  },
  data(){
    return {
        tasks: []
    }
  },
  methods:{
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