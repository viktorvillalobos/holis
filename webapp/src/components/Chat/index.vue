<template>
  <div class="connect-chat">
    <chat-header chat-name="Juanin Juan Harry" />
    <div class="connect-chat-body">
      <div class="nose"></div>
      <div class="connect-chat-body-messages-wrapper">
        <message v-for="msg in messages" :key="msg" :msg="msg" :messageIsMine="msg.is_mine" />
      </div>
    </div>
    <chat-editor @enter="sendMessage" />
  </div>
</template>

<script>
import ChatHeader from "./ChatHeader";
import ChatEditor from "./ChatEditor";
import Message from "./Message";
export default {
  name: "Chat",
  components: {
    ChatHeader,
    ChatEditor,
    Message
  },
  data() {
    return {
      messages: [
        {
          message: "Hola!",
          is_mine: false
        }
      ]
    };
  },
  methods: {
    sendMessage(msg) {
      console.log('msg', msg)
      this.messages.push(msg)
    }
  }
};
</script>

<style lang="scss" scoped>
.connect-chat {
  border-top: 1px solid $light-gray;
  position: relative;
  height: 100%;
  box-sizing: border-box;

  &-body {
    height: calc(100vh - 50px);
    overflow-y: scroll;
    padding: 40px 15px 0 15px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
    overflow-y: scroll;

    .nose {
      flex: 1 1 auto;
      min-height: 12px;
    }

    &-messages-wrapper {
      flex: 0 0 auto;
      display: flex;
      flex-direction: column;
    }
  }
}
</style>