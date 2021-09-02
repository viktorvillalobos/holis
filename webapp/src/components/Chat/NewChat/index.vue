<template>
    <div class="new-chat">
      <div class="header-new-chat columns pt-5 flx-1">
          <button class="button is-ghost column is-1" @click="goToInbox">
              <span class="icon is-small">
                  <span class="material-icons" style="color:#fff">chevron_left</span>
              </span>
          </button>
          <b class="column" style="color:#fff">New conversation</b>
          <!--<div class="column mr-5" align="right" style="cursor: pointer" @click="goToGroup">
            <span class="material-icons-round" style="color:white">forum</span> 
          </div>-->
      </div>
      <div class="tags ml-5 mr-5 flx-1" v-if="participants.length > 0">
        <span v-for="participant in participants" :key="participant.id" class="tag is-primary">
          {{participant.name.substring(0,50) || participant.username.substring(0,50)}}
          <button class="delete is-small" @click="selectParticipant(participant)"></button>
        </span>
      </div>
      <div class="field mr-5 ml-5 mt-4 flx-1">
          <p class="control has-icons-left has-icons-right">
              <input class="input input-chat" type="text" placeholder="Search user" @input="debounceInput">
              <span class="icon is-left">
                  <span class="material-icons" style="color:#2D343C">search</span>
              </span>
          </p>
      </div>
      <vue-scroll v-if="loading">
        <div v-for="index in 10" :key="index">
          <div class="column columns">
              <PuSkeleton class="ml-5" circle height="50px" width="50px"/>
              <div class="column">
                  <PuSkeleton height="20px" width="80%"  />
              </div>
          </div>
        </div>
      </vue-scroll>
      <vue-scroll class="flx-1" v-else>
        <div class="user-items" v-for="user in filterUsers" :key="user.id" @click="selectParticipant(user)"> <!-- @click="openChatUser(user)"-->
            <span class="icon-text">
                <span class="icon">
                    <Avatar v-if="user.avatar_thumb" :img="user.avatar_thumb"/>
                    <font-awesome-icon v-else icon="user-circle" size="3x"/>
                </span>
                <b class="header-new-chat-title">{{user.name.substring(0,50) || user.username.substring(0,50) }}</b>
            </span>
        </div>
      </vue-scroll>
      <div class="flx-1 m-5" v-if="participants.length > 0">
        <button class="button is-fullwidth is-primary" :class="{'is-loading' : loadingCreate}" @click="createGroup">Create conversation</button>
      </div>
      <div v-if="users.length == 0 && !firstLoad" style="display: flex; flex-direction: column; justify-content: center; align-items: center;" class="mt-6">
          <font-awesome-icon icon="sad-tear" size="6x"/>
          <p>No contact found</p>
      </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import Avatar from '@/components/Avatar'
import IconifyIcon from '@iconify/vue';
import magnifyIcon from '@iconify/icons-mdi/magnify'
import closeIcon from '@iconify/icons-mdi/close'
import Loading from '@/components/Loading'
import _ from 'lodash'

export default {
  name: 'InboxMessage',
  computed: {
    ...mapState({
      users: state => state.chat.users
    }),
    filterUsers(){
      return this.users.filter(user => this.participants.findIndex(participant => participant.id == user.id) == -1)
    }
  },
  data () {
    return {
      loading: false,
      loadingCreate: false,
      icons: {
        magnifyIcon: magnifyIcon,
        closeIcon: closeIcon
      },
      firstLoad: true,
      participants: [],
    }
  },
  watch:{
      users (newVal){
          this.firstLoad = false
          this.loading = false
      }
  },
  components: {
      Avatar,
      IconifyIcon,
      Loading
  },
  methods:{
      debounceInput: _.debounce(function (e) {
        this.loading = true
        this.$store.dispatch('getUsers', e.target.value)
      }, 300),
      goToInbox(){
        this.$store.commit('setCurrentChatName', null)
        this.$store.commit('setCurrentChatID', null)
        this.$store.commit('setScreenChat', 'inbox')
      },
      goToGroup(){
        this.$store.commit('setCurrentChatName', null)
        this.$store.commit('setCurrentChatID', null)
        this.$store.commit('setScreenChat', 'newgroup')
      },
      selectParticipant(recent){
        const index = this.participants.findIndex(element => element.id == recent.id)
        if(index == -1){
            this.participants.push(recent)
        }else{
            this.participants.splice(index, 1)
        }
      },
      openChatUser(recent){
          console.log(recent)
        const data = {
            to: recent.id,
            first_time: true,
            new_chat : true
        }
        this.$store.dispatch('getMessagesByUser', data)
        this.$store.commit('setCurrentChatName', recent.name)
      },
      createGroup(){
        this.loadingCreate = true
        const ids = []
        var nameChat = ""
        this.participants.forEach((element, index) => {
            ids.push(element.id)
            nameChat += element.name
            if(index > 0)
              nameChat += ", "
        })
        const data = {
            to: ids,
            first_time: true,
            new_chat : true
        }
        console.log(data)
        this.$store.dispatch('getMessagesByGroup', data)
        this.$store.commit('setCurrentChatName', nameChat)
      }
  },
  created(){
      this.loading = true
      this.$store.dispatch('getUsers', "")
  }
}
</script>

<style lang="scss">
.new-chat{
  display: flex;
  flex-direction: column;
  height: 100%;

  &-flx-1{
    flex: 1;
  }

  &-flx-0{
    flex: 0;
  }
}

.header-new-chat {
  font-family: $family-dm-sans;
  background: #364DFF;
  margin-left: 0px !important;
  padding-left: 0px;
  height: 90px;
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

.tags{
  margin-top: 10px !important;
  margin-bottom: 0px !important;
}

/*.input{
    background-color: transparent !important;
    border-color: #ffffff !important;
    color: #ffffff !important;
}*/

//$input-placeholder-color: #fff;
</style>
