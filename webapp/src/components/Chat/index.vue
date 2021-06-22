<template>
  <div class="connect-chat" :style="`background-image: url(${patternChat})`">
    <div v-if="chatActive" class="connect-chat-new">
      <h3>Nuevo mensaje</h3>
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Para:</label>
        </div>
        <div class="field-body">
          <div class="field">
            <p class="control">
              <input class="input is-small" type="text" placeholder />
            </p>
          </div>
        </div>
      </div>
      <card class="connect-chat-new-frequent-chats">
        <ul>
          <li v-for="user in users" :key="user.id" @click="setChat(user)">
            <Avatar :img="user.avatar_thumb" />
            <span class="user-name">{{user.name || user.username}}</span>
          </li>
        </ul>
      </card>
    </div>
    <chat-header v-if="!chatActive" :chat-name="currentChatName" />
    <div
      v-if="!chatActive"
      class="connect-chat-body"
    >

      <button
        class="button is-dark is-rounded load-more"
        v-if="showLoadHistory"
        @click="loadHistory()">Load history</button>

      <vue-scroll ref="chatContainer"
                  @handle-scroll="handleScroll">
        <div class="connect-chat-body-messages-wrapper">
          <message
            v-for="msg in messages"
            :key="msg.id"
            :message="msg"
          />
        </div>
      </vue-scroll>
    </div>
    <Loading v-bind:loading="loading"/>
    <chat-editor v-if="!chatActive" @enter="sendMessage" />
  </div>
</template>

<script>
import { mapState } from 'vuex'

import ChatHeader from './ChatHeader'
import ChatEditor from './ChatEditor'
import Message from './Message'
import Avatar from '@/components/Avatar'
import Card from '@/components/Card'
import pattern from '@/assets/lighter_pattern.png'
import Loading from '@/components/Loading'

export default {
  name: 'Chat',
  components: {
    ChatHeader,
    ChatEditor,
    Message,
    Avatar,
    Card,
    Loading
  },
  data () {
    return {
      searchPerson: '',
      jid: '',
      patternChat: pattern,
      isLoadingHistory: false,
      showLoadHistory: false,
      savePosition: 0,
      loading: true
    }
  },
  computed: {
    ...mapState({
      users: state => state.chat.users,
      messages: state => state.chat.messages,
      next: state => state.chat.next,
      allowScrollToEnd: state => state.chat.allowScrollToEnd,
      currentChatJID: state => state.chat.currentChatJID,
      currentChatName: state => state.chat.currentChatName,
      chatActive: state => state.chat.chatActive
    })
  },
  watch: {
    messages (newVal) {
      if (newVal.length == 0) {
        this.isFirstTime = true // Esta comprobacion forza para que la primera vez para que haga scroll
        return
      }

      this.loading = false

      if(!this.isLoadingHistory){
        setTimeout(() => {
          this.scrollToEnd()
        }, 400)
      }else{
        this.isLoadingHistory = false 
      }
    },
    chatActive (newVal) {
      this.isFirstTime = true
    }
  },
  mounted () {
    // this.scrollToEnd()
  },
  updated () {
    if (this.allowScrollToEnd) {
      // this.scrollToEnd()
    }
  },
  methods: {
    handleScroll (vertical, horizonal, nativeEvent) {
      if (this.next && vertical.process <= 0.06) { this.showLoadHistory = true } else { this.showLoadHistory = false }

      const content = this.$refs.chatContainer
      if (
        content &&
        content.scrollTop === 0 &&
        this.next
      ) {
        setTimeout(() => {
          this.loadHistory()
          content.scrollTop = 1200
        }, 400)
      }
    },
    loadHistory () {
      if (this.next) {
        // this.savePosition = this.$refs.chatContainer.getPosition()
        this.$store.dispatch('getNextMessages')
        this.isLoadingHistory = true
      }
    },
    scrollToEnd () {
      const content = this.$refs.chatContainer
      console.log('SOLAAAA', content.scrollHeight)

      if (content) content.scrollTo({ y: '100%' }, content.scrollHeight)
    },
    addMessage (msg) {
      this.messages.push(msg)
    },
    sendMessage (msg) {
      console.log('msg', msg)
      this.$store.dispatch('sendChatMessage', { msg })
      this.scrollToEnd()
    },
    setChat (user) {
      console.log('hey!')
      console.log(user)
      this.$emit('selectedChat')
      this.$store.commit('setCurrentChatName', user.name || user.username)
      this.$store.commit('setCurrentChatID', user.id)
      const data = {
        to: user.id,
        first_time: true
      }
      this.$store.dispatch('getMessagesByUser', data)
    }
  }
}
</script>

<style lang="scss">
.load-more{
  width: 140px;
  margin: auto;
  margin-top: 10px;
  margin-bottom: 10px;
  position: absolute;
}
.connect-chat {
  border-top: 1px solid $light-gray;
  position: relative;
  height: 100%;
  box-sizing: border-box;

  &-load-more {
    color: #4f4f4f;
    text-align: center;
    cursor: pointer;
    text-decoration: underline;
    font-size: 0.8rem;
    margin-bottom: 2%;
  }

  &-new {
    padding: 4px 15px;
    position: relative;
    z-index: 99;

    h3 {
      font-weight: 700;
    }

    .field-label label {
      font-weight: 400;
      font-size: 12px;
    }

    .input {
      background: $light-gray;
      border-color: transparent;
    }

    &-frequent-chats {
      position: absolute;
      width: calc(100% - 100px);
      top: 100%;
      left: 88px;
      z-index: 8;

      ul {
        li {
          width: 100%;
          display: flex;
          align-items: center;
          padding: 5px 8px;

          .user-name {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }

          &:hover {
            background: $light-gray;
            cursor: pointer;
          }

          .connect-avatar {
            margin-right: 10px;
            width: 30px;
            height: 30px;
          }
        }
      }
    }
  }

  &-body {
    height: calc(100vh - 100px);
    padding: 40px 0 0 0;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;

    .nose {
      flex: 1 1 auto;
      min-height: 12px;
    }

    &-messages-wrapper {
      flex: 0 0 auto;
      display: flex;
      flex-direction: column;
      padding: 0 15px;
    }
  }
}
</style>
