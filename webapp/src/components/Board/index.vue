<template>
  <div class="connect-board">
    <birthdays />
    <div class="connect-board-posts-wrapper">
      <Post
        v-for="post in announcementsList"
        :key="post.id"
        :isPinned="post.isPinned"
        :author="post.created_by"
        :post="post"
      ></Post>
      <transition name="translate-x">
        <PostEditor v-if="postEditorIsActive" :instance="instance" @close="handlePostEditor" />
      </transition>
    </div>
    <transition name="translate-y">
      <PostCTA v-if="!postEditorIsActive" @action="handlePostEditor" />
    </transition>
  </div>
</template>
<script>
import {mapState} from 'vuex';

import Birthdays from "./Birthdays";
import Post from "./Post";
import PostCTA from "./PostCTA";
import PostEditor from "./PostEditor";
export default {
  name: "Board",
  components: {
    Birthdays,
    Post,
    PostCTA,
    PostEditor
  },
  data() {
    return {
      postEditorIsActive: false,
      instance: {},
      posts: [
        {
          id: 1,
          title: "¡Chao jefe! Ahora vendo empanadas",
          isPinned: false,
          date: new Date(),
          content:
            "Bueno yo vengo a hacer este post para comentarles a todos todos que la verdad es que yo vendo empanadas y me quedan bien bien ricas odio mi trabajo en la oficina y me gustaría independizarme así que si alguien me quiere comprar empanaditas que sepa que tengo de pollo, de carne, tengo empanadas light, tengo enmpanadas de queso, empanada venezolana, venezolana integral, chilena, argentina, pida nomás que aquí hay. Les dejo mi número +569123123123  ",
          author: {
            name: "Juan Pablo",
            position: "Mobile Dev"
          }
        },
        {
          id: 2,
          title: "Nuevas funcionalidades en la app",
          isPinned: false,
          date: new Date(),
          content:
            "Hola a todos! Espero estén bien a gusto. Les anuncio a todos que tenemos nuevas funcionalidades bien bknes en la app. Ahora pueden:* Volar* Teletransportarse* Sacar la vuelta sin que nadie se entere...",
          author: {
            name: "Juan Pablo",
            position: "Mobile Dev"
          }
        }
      ]
    };
  },
  computed: {
    ...mapState({
      announcementsList: state => state.announcements.list.results 
    })
  },
  methods: {
    handlePostEditor() {
      this.postEditorIsActive = !this.postEditorIsActive;
      this.instance = {}
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-board {
  padding: 9px;
  position: relative;
  box-sizing: border-box;
  height: calc(100vh - 42px);

  &-posts-wrapper {
    height: calc(100vh - 140px);
    overflow-y: auto;
    box-sizing: border-box;
    position: relative;
    margin-top: 5px;

    > div:last-child:not(.connect-board-post-editor) {
      margin-bottom: 100px;
    }
  }
}
</style>
