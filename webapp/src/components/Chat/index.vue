<template>
  <div class="connect-chat">
    <chat-header chat-name="Juanin Juan Harry" />
    <div class="connect-chat-body"></div>
    <chat-editor />
  </div>
</template>

<script>
import ChatHeader from "./ChatHeader";
import ChatEditor from "./ChatEditor";
export default {
  name: "Chat",
  components: {
    ChatHeader,
    ChatEditor
  }
};
</script>

<style lang="scss" scoped>
.connect-chat {
  border-top: 1px solid $light-gray;
  position: relative;
  height: calc(100vh - #{$user-card-space});
  box-sizing: border-box;

  &-body {
    height: calc(100vh - #{$user-card-space + 37px});
    padding: 0 15px;
  }
}
</style>