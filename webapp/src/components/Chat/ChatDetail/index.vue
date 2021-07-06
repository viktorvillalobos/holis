<template>
  <div class="connect-chat"> <!-- :style="`background-image: url(${patternChat})`" -->
    <chat-header :chat-name="currentChatName" />
    <div
      class="connect-chat-body"
    >
      <button
        class="button is-dark is-rounded load-more"
        v-if="showLoadHistory"
        @click="loadHistory()">Load history</button>

      <vue-scroll ref="chatContainer"
                  @handle-scroll="handleScroll">
        <div class="connect-chat-body-messages-wrapper">
          <div v-for="msg in messages" :key="msg.id">

            <div class="chat-divider" style="position:absolute"></div>

            <div v-if="msg.showDate" class="card date-message">
              <div class="card-content">
                <div class="content">
                  {{ dateMessage(msg.created) }}
                </div>
              </div>
            </div>
            <message
              :id="msg.created"
              :message="msg"
            />
          </div>
        </div>
      </vue-scroll>
    </div>
    <Loading v-bind:loading="loading"/>
    <chat-editor 
          ref="chatContainer2"
          @sendMessage="sendMessage"
    />
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
import moment from 'moment'

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
      loading: true,
      observer: null,
      isFirstTime: true,
      dateMsg: '',
    }
  },
  created(){
  },
  computed: {
    ...mapState({
      users: state => state.chat.users,
      messages: state => state.chat.messages,
      next: state => state.chat.next,
      allowScrollToEnd: state => state.chat.allowScrollToEnd,
      currentChatID: state => state.chat.currentChatID,
      currentChatName: state => state.chat.currentChatName,
      app: state => state.app.user
    })
  },
  watch: {
    messages (newVal) {
      if(!this.isLoadingHistory){
        setTimeout(() => {
          this.scrollToEnd()
        }, 400)
      }else{
        this.isLoadingHistory = false 
      }
      this.loading = false
    },
    chatActive (newVal) {
      this.isFirstTime = true
    }
  },
  mounted () {
    // this.scrollToEnd()
    //const aaa = this.$refs.chatContainer2
    //console.log("TUNDIIIII"+JSON.stringify(aaa))
    //this.initObserver()
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
      //console.log("currentView", content.getCurrentviewDom()[0].id)
      //const dateTest = content.getCurrentviewDom()[0].id
      //this.prepareDate(dateTest)
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
    dateMessage(date){
      return this.prepareDate(date)
    },
    prepareDate(date){
      console.log(date)
      const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
      const firstDate = new Date(date);
      const secondDate = new Date();

      const diffDays = Math.round(Math.abs((firstDate - secondDate) / oneDay));

      if(diffDays > 2)
        return moment(date).format('L')
      
      return moment(date).fromNow()
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
    },
    onResize() {
        const box = this.$refs.chatContainer2,
          vm = this
        let { width, height } = box.style

        this.width = width
        this.height = height
        console.log("cambioooooo"+height)
        // Optionally, emit event with dimensions
        //this.$emit('resize', { width, height })
    },
    initObserver() {
        const config = {
            attributes: true,
          },
          vm = this
        const observer = new MutationObserver(function (mutations) {
          mutations.forEach(function (mutation) {
            if (mutation.type === 'attributes') {
              vm.onResize()
            }
          })
        })
        observer.observe(this.$refs.chatContainer2, config)
        this.observer = observer
      },
  }
}
</script>

<style lang="scss">

.chat-divider{
    width: 100%;
    height: 0px;
    border: 1px solid #F7F7F7;
}

.flexbox-chat{
  height: 100%; 
    display: flex;
    flex-flow: column nowrap;
    align-items: stretch;
}

.date-message{
  width: 140px;
  margin: auto;
  margin-top: -30px;
  position: absolute;
  background: transparent;
}

.load-more{
  width: 140px;
  margin: auto;
  margin-top: 10px;
  margin-bottom: 10px;
  position: absolute;
  background: transparent;
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
