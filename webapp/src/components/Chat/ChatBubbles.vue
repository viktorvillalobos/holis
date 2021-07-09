<template>
  <ul :class="['connect-chat-bubbles', {'aside-opened': asideOpened}]">
    <li>
      <Btn @btn-click="emitAsideHandle" :size="40" primary round icon>
        <span v-if="asideOpened" class="material-icons md-16" style="color:#fff">chevron_right</span>
        <span v-else class="material-icons md-16" style="color:#fff">chevron_left</span>
      </Btn>
    </li>
    <li>
      <Btn :size="40" primary round icon @btn-click="openNewChat" >
        <span class="material-icons" style="color:#fff; font-size: 17px;">chat</span>
      </Btn>
    </li>
    <!--
      Comentando chat recientes
      <li class="history-chat"
        v-for="recent in recents"
        :key="recent.id"
        @click="handleHistoryChat(recent)">
      <Avatar :img="recent.avatar_thumb" :text="recent.name"/>
    </li>--> 
  </ul>
</template>
<script>
import Avatar from '@/components/Avatar'
import Btn from '@/components/Btn'
import { mapState } from 'vuex'

export default {
  name: 'ChatBubbles',
  props: {
    asideOpened: {
      type: Boolean
    }
  },
  components: {
    Avatar,
    Btn
  },
  computed: {
    ...mapState({
      recents: state => state.chat.recents,
      currentChatID: state => state.chat.currentChatID,
      currentChatName: state => state.chat.currentChatName,
      isAsideRightActive: state => state.app.isAsideRightActive
    })
  },
  methods: {
    handleHistoryChat (recent) {
      this.$store.commit('setAsideRightActive', true)
      this.$store.commit('setChatActive', false)
      this.$store.commit('clearMessages')
      const data = {
        to: recent.id,
        first_time: true
      }
      this.$store.dispatch('getMessagesByUser', data)
      this.$store.commit('setCurrentChatName', recent.name)
      this.$store.commit('setCurrentChatID', recent.id)
    },
    emitAsideHandle () {
      if (this.isAsideRightActive) {
        this.$store.commit('setAsideRightActive')
        return
      }

      this.clearChat()
      this.$store.commit('setInboxActive', true)
      this.$store.commit('setAsideRightActive')
    },
    openNewChat () {
      this.clearChat()
      this.$store.commit('setInboxActive', false)
      this.$store.commit('setAsideRightActive', true)
    },
    clearChat(){
      this.$store.commit('setCurrentChatName', null)
      this.$store.commit('setCurrentChatID', null)
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-chat-bubbles {
  position: fixed;
  bottom: 11px;
  right: $margin-left-container;
  width: 45px;
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: $aside-transition;
  z-index: 14;

  &.aside-opened {
    right: $margin-right-container-aside-opened;
  }

  li {
    margin: 7px 0;
    cursor: hover;
  }
}

li {
  cursor: pointer;
}
</style>
