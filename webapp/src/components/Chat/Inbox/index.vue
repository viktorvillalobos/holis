<template>
  <div>
    <Loading v-bind:loading="loading"/>
    <div class="header-inbox">
      <div class="columns" style="height:80px">
          <div class="column columns">
              <Avatar class="column" :img="user ? user.avatar || user.avatar_thumb : null" />
              <div class="column avatar-titles">
                  <b>{{user ? user.name : 'Nombre misterioso' }}</b>
                  <p>{{user ? user.position: 'Cargo misterioso'}}</p>
              </div>
          </div>
          <div class="column columns" style="justify-content: flex-end;">
            <button class="button is-ghost is-1" @click="openNewChat">
              <span class="icon is-small">
                 <span class="material-icons" style="color:#fff">add_comment</span>
              </span>
            </button>
          </div>
      </div>
      <div class="field">
        <p class="control has-icons-left has-icons-right">
          <input class="input input-inbox" placeholder="Search person or group" @input="debounceInput">
          <span class="icon is-left">
            <span class="material-icons" style="color:#fff">search</span>
          </span>
          <span class="icon is-right" style="cursor: pointer;" v-if="query.length > 0">
            <span class="material-icons" style="color:#fff" >close</span>
          </span>
        </p>
      </div>
    </div>
    <div v-if="recents && recents.length > 0">
      <div v-for="recent in recents" :key="recent.id" @click="openChatUser(recent)">
        <InboxMessage v-bind:recent="recent"/>
      </div>
    </div>
    <div v-if="recents && recents.length == 0 && !firstLoad" style="display: flex; flex-direction: column; justify-content: center; align-items: center;" class="mt-6">
      <font-awesome-icon icon="sad-tear" size="6x"/>
      <p>No contact found</p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Loading from '@/components/Loading'
import Avatar from '@/components/Avatar'
import InboxMessage from './Inbox'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import _ from 'lodash'

export default {
  name: 'Inbox',
  components: {
    Loading,
    Avatar,
    InboxMessage,
    FontAwesomeIcon
  },
  data () {
    return {
      loading: false,
      query: "",
      firstLoad: true
    }
  },
  computed: {
    ...mapState({
      messages: state => state.chat.messages,
      user: state => state.app.user,
      recents: state => state.chat.recents.results,
    })
  },
  methods:{
    debounceInput: _.debounce(function (e) {
      this.getInbox(e.target.value)
    }, 300),
    openNewChat () {
      this.$store.commit('setCurrentChatName', null)
      this.$store.commit('setCurrentChatID', null)
      this.$store.commit('setInboxActive', false)
      this.$store.commit('setAsideRightActive', true)
    },
    openChatUser(recent){
      const data = {
        to: recent.to_user_id,
        first_time: true
      }
      this.$store.dispatch('getMessagesByUser', data)
      this.$store.commit('setCurrentChatName', recent.to_user_name )
      this.$store.commit('setCurrentChatID', recent.uuid)
    },
    getInbox(search = ""){
      try {
        //this.$store.commit('setRecents', [])
        this.loading = true
        this.$store.dispatch('getRecents',search)
      } catch (e) {
        console.log('couldnt load recents')
      }
    }
  },
  mounted(){
    this.getInbox()
  },
  watch: {
    recents (newVal) {
      console.log("RECIENTESSS",newVal)
      this.loading = false
      this.firstLoad = false
    }
  }
}
</script>

<style lang="scss">

.header-inbox {
  font-family: $family-dm-sans;
  padding: 40px;
  background: #364DFF;
  //background: linear-gradient(90deg, #364DFF 0%, #5165FF 100%);
  box-shadow: 0px 4px 4px rgba(224, 224, 224, 0.1);
}

.input-inbox{
    background-color: transparent !important;
    border-color: #fff !important;
    color: #fff !important;
}

::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: #fff !important;
  opacity: 1 !important; /* Firefox */
}

:-ms-input-placeholder { /* Internet Explorer 10-11 */
  color: #fff !important;
}

::-ms-input-placeholder { /* Microsoft Edge */
  color: #fff !important;
}

.avatar-titles{
  margin-left: 15px;
  color: #fff;
  &-b{
    size: 14px;
  }
  &-p{
    size: 12px;
  }
}

.items-right{
   float: right;
   clear: both;
}

.icons-header{
  margin-right: -25px;

 &:hover{
   cursor: pointer;

    svg:not(.non-lineal) path {
      fill: $primary;
    }

    svg.non-lineal path {
      fill: none;
      stroke: $primary;
    }
 }

}

</style>
