<template>
    <div>
        <div class="header-new-chat columns pt-5">
            <button class="button is-ghost column is-1" @click="goToInbox">
                <span class="icon is-small">
                    <span class="material-icons" style="color:#fff">chevron_left</span>
                </span>
            </button>
            <b class="column" style="color:#fff">New message</b>
        </div>
        <div class="field mr-5 ml-5 mt-5">
            <p class="control has-icons-left has-icons-right">
                <input class="input input-chat" type="text" placeholder="Search or start a new conversation" v-model="query">
                <span class="icon is-left">
                    <span class="material-icons" style="color:#2D343C">search</span>
                </span>
                <span class="icon is-right" v-if="query.length > 0" @click="clickPrueba">
                    <span class="material-icons" style="color:#2D343C">close</span>
                </span>
            </p>
        </div>
        <div class="user-items" v-for="user in users" :key="user.id" @click="openChatUser(user)">
            <span class="icon-text">
                <span class="icon">
                    <Avatar v-if="user.avatar_thumb" :img="user.avatar_thumb"/>
                    <font-awesome-icon v-else icon="user-circle" size="3x"/>
                </span>
                <b class="header-new-chat-title">{{user.name || user.username}}</b>
            </span>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import Avatar from '@/components/Avatar'
import IconifyIcon from '@iconify/vue';
import magnifyIcon from '@iconify/icons-mdi/magnify'
import closeIcon from '@iconify/icons-mdi/close'

export default {
  name: 'InboxMessage',
  computed: {
    ...mapState({
      users: state => state.chat.users
    })
  },
  watch:{
      users (newVal){
          console.log("entreeee5",newVal)
      }
  },
  components: {
      Avatar,
      IconifyIcon
  },
  methods:{
      goToInbox(){
        this.$store.commit('setCurrentChatName', null)
        this.$store.commit('setCurrentChatID', null)
        this.$store.commit('setInboxActive', true)
      },
      openChatUser(recent){
        const data = {
            to: recent.id,
            first_time: true
        }
        this.$store.dispatch('getMessagesByUser', data)
        this.$store.commit('setCurrentChatName', recent.name)
        this.$store.commit('setCurrentChatID', recent.id)
      },
      clickPrueba(){
          console.log("PRUEBAAAA")
      }
  },
  data () {
    return {
        query: "",
        icons: {
            magnifyIcon: magnifyIcon,
            closeIcon: closeIcon
        },
    }
  },
  created(){
      console.log("Entre")
      this.$store.dispatch('getUsers')
  }
}
</script>

<style lang="scss">
.header-new-chat {
  font-family: $family-dm-sans;
  background: #364DFF;
  margin-left: 0px !important;
  padding-left: 0px;
  height: 80px;
  //background: linear-gradient(90deg, #364DFF 0%, #5165FF 100%);
  box-shadow: 0px 4px 4px rgba(224, 224, 224, 0.1);

    &-title{
        max-lines: 1;
        margin-left:20px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 1; /* number of lines to show */
        -webkit-box-orient: vertical;
    }
}

.user-items{
    padding: 20px 40px 20px 40px;
}

.user-items:hover{
    cursor: pointer;
    background-color: rgba(128, 128, 128, 0.5);
}

.input-chat{
    background-color: transparent !important;
    border-color: #BDBDBD !important;
    color: #BDBDBD !important;
}

::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: #BDBDBD !important;
  opacity: 1 !important; /* Firefox */
}

:-ms-input-placeholder { /* Internet Explorer 10-11 */
  color: #BDBDBD !important;
}

::-ms-input-placeholder { /* Microsoft Edge */
  color: #BDBDBD !important;
}

/*.input{
    background-color: transparent !important;
    border-color: #ffffff !important;
    color: #ffffff !important;
}*/

//$input-placeholder-color: #fff;
</style>
