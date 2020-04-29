<template>
  <div class="connect-board-post-editor">
    <label>Título</label>
    <input v-model="instance.title" type="text" />
    <label>Contenido</label>
    <textarea v-model="instance.content" name id cols="30" rows="10"></textarea>
    <ul>
      <li>
        <Btn @btn-click="handleClose" flat>Cancelar</Btn>
      </li>
      <li>
        <Btn primary>Anunciar</Btn>
      </li>
    </ul>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
export default {
  name: "PostEditor",
  props: {
    instance: {
        type: Object
    }
  },
  components: {
    Btn
  },
  methods: {
    handleClose() {
      this.$emit('close')
    }
  }
};
</script>
<style lang="scss" scoped>
@import "../../assets/variables";
.connect-board-post-editor {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  padding: 10px 0;
  box-sizing: border-box;

  > * {
    width: 315px;
    box-sizing: border-box;
  }

  label {
    display: block;
    margin: 15px 0 7px 0;
  }

  textarea,
  input {
    border-radius: 4px;
    border: 1px solid $light-gray;
    resize: vertical;
    padding: 5px;
    color: $font-color;
    font-family: "Ubuntu", sans-serif;
  }

  ul {
    padding: 0;
    margin: 10px 0;
    display: inline-flex;
    list-style: none;
    align-items: center;
    justify-content: flex-end;

    li {
      display: inline-flex;
      margin-left: 10px;
    }
  }
}
</style>