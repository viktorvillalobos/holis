<template>
  <div class="card ml-4 mb-3 hover-card" @click="openProjectDetail">
        <div class="card-content">
            <div class="media">
                <!--<div class="media-left mt-4">
                    <img class="connect-logo-company" src="/static/images/logo/logo.svg" alt="espazum logo" width="60"/>
                </div>-->
                <div class="media-content">
                    <b class="is-size-6">{{ project.name}}</b>
                    <p class="is-size-7">Team: {{ project.getMembers() }}</p>
                    <p class="is-size-7" v-if="project.end_date">Final date: {{ project.end_date }}</p>
                </div>

                <div class="media-right" align="right">
                    <!--<div>
                        <button class="button is-danger is-light is-small alert-days">15 tareas abiertas</button>
                        <button class="button is-success is-light is-small alert-days">15 días restantes</button>
                    </div>-->
                    <div>
                       <span class="material-icons-round mt-5" style="color: #828282">chevron_right</span>
                        <!--<button class="button is-danger is-inverted is-small" @click.stop="deleteProject">Borrar</button>-->
                        <!--<button class="button is-primary is-inverted is-small">Editar</button>
                        <button class="button is-primary is-inverted is-small">Ver más</button>-->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Card from '@/components/Card'
import Btn from '@/components/Btn'
export default {
  name: 'Project',
  props: ['project'],
  components: {
    Card,
    Btn
  },
  methods: {
    deleteProject () {
      console.log('Falta implementacion')
    },
    openProjectDetail () {
      this.$store.commit('setCurrentScreen', { screen: 'detail', data: this.project })
    }
  }
}
</script>
<style lang="scss" scoped>
.alert-days{
    padding: 2px;
    margin-left: 5px;
}

.hover-card{
  font-family: $family-dm-sans;
   box-shadow: 0px 0px 0px grey;
  -webkit-transition:  box-shadow .6s ease-out;
  transition: box-shadow .6s ease-out;
  box-shadow: .8px .9px 3px grey; 
}
.hover-card:hover{
     box-shadow: 1px 8px 10px grey;
    -webkit-transition:  box-shadow .6s ease-in;
    transition: box-shadow .6s ease-in;
}
</style>
