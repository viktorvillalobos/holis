<template>
  <div class="connect-chat-header">
    <div class="columns">
        <button class="button is-ghost column is-1" @click="goToInbox">
            <span class="icon is-small">
                <span class="material-icons" style="color:#fff">chevron_left</span>
            </span>
        </button>
        <b class="column" style="color:#fff">{{chatName}}</b>
    </div>
<!---    <ul class="chat-actions">
      <li>
        <font-awesome-icon icon="search" @click="handleSearch"/>
      </li>

      <li>
        <font-awesome-icon icon="plus" />
      </li>
    </ul>-->
  </div>
</template>
<script>
export default {
  props: {
    chatName: {
      type: String,
      default: 'Chat name'
    }
  },
  methods: {
    handleSearch () {
      this.$store.commit('clearMessages')
      this.$store.commit('setChatActive', true)
    },
    goToInbox(){
        this.$store.commit('setCurrentChatName', null)
        this.$store.commit('setCurrentChatID', null)
        this.$store.commit('setInboxActive', true)
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 10px 15px 10px 15px;
  overflow: hidden;
  z-index: 99;
  color: #fff;
  background-color: #364DFF;

  .svg-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 15;

    svg {
      position: absolute;
      bottom: 0;
    }
  }

  h3 {
    font-weight: 600;
    position: relative;
    z-index: 30;
  }

  .chat-actions {
    position: relative;
    z-index: 30;
    display: flex;
    align-items: center;
    justify-content: flex-end;

    li {
      margin-left: 5px;
      cursor: pointer;
      border-radius: 50%;
      width: 24px;
      text-align: center;

      &:hover {
        background: rgba(0, 0, 0, 0.2);
      }
    }
  }
}
</style>
