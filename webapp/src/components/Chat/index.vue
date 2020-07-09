<template>
  <div class="connect-chat">
    <div v-if="newChat" class="connect-chat-new">
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
            <Avatar :img="user.avatar_thumb" /> <span class="user-name">{{user.name || user.username}}</span>
          </li>
        </ul>
      </card>
    </div>
    <chat-header v-if="!newChat" :chat-name="chatName" />
    <div v-if="!newChat"
         class="connect-chat-body"
        ref="chatContainer">
      <div class="nose"></div>
      <span class="connect-chat-load-more">Load history</span>
      <div  class="connect-chat-body-messages-wrapper">
        <message v-for="(msg, idx) in messages"
                :key="idx"
                :msg="msg"
                :messageIsMine="msg.is_mine"
                :who="msg.who"
                :datetime="msg.datetime"
        />
      </div>
    </div>
    <chat-editor v-if="!newChat" @enter="sendMessage" />
  </div>
</template>

<script>
import { mapState } from 'vuex'

import ChatHeader from './ChatHeader'
import ChatEditor from './ChatEditor'
import Message from './Message'
import Avatar from '@/components/Avatar'
import Card from '@/components/Card'

export default {
  name: 'Chat',
  components: {
    ChatHeader,
    ChatEditor,
    Message,
    Avatar,
    Card
  },
  props: {
    newChat: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      searchPerson: '',
      chatName: 'Juanin Juan Harry',
      jid: ''
    }
  },
  computed: {
    ...mapState({
      users: state => state.chat.users,
      messages: state => state.chat.messages
    })
  },
  mounted () {
    this.$store.dispatch('connectXMPP')
    this.scrollToEnd()
  },
  updated () {
    this.scrollToEnd()
  },
  methods: {
    scrollToEnd () {
      const content = this.$refs.chatContainer
      if (content) content.scrollTop = content.scrollHeight
    },
    addMessage (msg) {
      this.messages.push(msg)
    },
    sendMessage (msg) {
      console.log('msg', msg)
      const data = {
        to: this.jid,
        msg: msg
      }
      this.$store.dispatch('sendChatMessage', data)
    },
    setChat (user) {
      console.log('hey!')
      this.$emit('selectedChat')
      this.jid = user.jid
      this.chatName = user.name || user.username
      this.$store.dispatch('getMessages', this.jid)
    }
  }
}
</script>

<style lang="scss">
.connect-chat {
  border-top: 1px solid $light-gray;
  position: relative;
  height: 100%;
  box-sizing: border-box;

  &-load-more {
    color: #4f4f4f;
    text-align:center;
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
