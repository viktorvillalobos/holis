<template>
  <div>
    <div align="right">
        <div class="select is-small is-primary mr-2">
            <select>
            <option>Todos</option>
            <option>Activos</option>
            <option>Cerrados</option>
            <option>Futuros</option>
            </select>
        </div>
    </div>
    <div align="center" :class="{'loader-wrapper' : true, 'is-active' : loading}">
        <div class="loader is-loading"></div>
    </div>
    <Project v-for="project in projects" :key="project.id"/>
  </div>
</template>
<script>
import Project from './Project'
import { mapState } from 'vuex'
export default {
  name: "ProjectList",
  components: {
    Project
  },
  props: ['type'],
  data(){
      return {
        loading: false
      }
  },
  created(){
    this.getProjects()
  },
  computed: {
    ...mapState({
      projects: state => state.projects.projects
    })
  },
  methods:{
    getProjects(){
      this.loading = true
      this.$store.dispatch('getProjects', this.type)
    }
  },
  watch: {
    type: function (newType, oldType) {
        this.getProjects()
    },
    projects: function(newType){
      setTimeout(() => {  this.loading = false }, 2000);
    }
  }
};
</script>

<style lang="scss" scoped>
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