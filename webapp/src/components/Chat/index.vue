<template>
  <div class="connect-chat"> <!-- :style="`background-image: url(${patternChat})`" -->
    <transition name="slide-fade">
      <HeaderInbox v-if="screenChat == 'inbox' && currentChatID == null"/>
    </transition>
    <transition name="slide-fade">
      <NewChat v-if="screenChat == 'newchat' && currentChatID == null"/>
    </transition>
    <transition name="slide-fade">
      <ChatDetail v-if="currentChatID"/>
    </transition>
     <transition name="slide-fade">
      <NewGroup v-if="screenChat == 'newgroup'" />
    </transition>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import Avatar from '@/components/Avatar'
import Card from '@/components/Card'
import pattern from '@/assets/lighter_pattern.png'
import HeaderInbox from './Inbox'
import NewChat from './NewChat'
import ChatDetail from './ChatDetail'
import NewGroup from './NewChatGroup'
import ChatScreen from './../../models/chatScreen'

export default {
  name: 'Chat',
  components: {
    Avatar,
    Card,
    HeaderInbox,
    NewChat,
    ChatDetail,
    NewGroup
  },
  data () {
    return {}
  },
  computed: {
    ...mapState({
      messages: state => state.chat.messages,
      next: state => state.chat.next,
      allowScrollToEnd: state => state.chat.allowScrollToEnd,
      currentChatID: state => state.chat.currentChatID,
      currentChatName: state => state.chat.currentChatName,
      screenChat: state => state.chat.screenChat,
      app: state => state.app.user
    })
  },
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
    height: calc(100vh - 120px);
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
      padding: 30px 15px 0px 15px;
    }
  }
}

.slide-fade-enter-active {
  transition: all .3s ease;
}
.slide-fade-leave-active {
  transition: all .3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(10px);
  opacity: 0;
}
</style>
