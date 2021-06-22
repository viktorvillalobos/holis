<template>
  <div>
    <div class="header-inbox">
      <div class="columns">
          <div class="column columns">
              <Avatar class="column" :img="user ? user.avatar || user.avatar_thumb : null" />
              <div class="column avatar-titles">
                  <b>{{user ? user.name : 'Nombre misterioso' }}</b>
                  <p>{{user ? user.position: 'Cargo misterioso'}}</p>
              </div>
          </div>
          <div class="column columns" style="justify-content: flex-end;">
            <span class="material-icons column is-one-fifth icons-header" style="color:#fff" >add_comment</span>
            <!--<iconify-icon :icon="icons.newChatIcon" style="color:#fff" class="column is-one-fifth icons-header"/>
            <iconify-icon :icon="icons.newGroupIcon" style="color:#fff" class="column is-one-fifth icons-header"/>-->
          </div>
      </div>
      <div class="field">
        <p class="control has-icons-left has-icons-right">
          <input class="input is-focused" placeholder="Search person or group">
          <span class="icon is-left">
            <iconify-icon :icon="icons.magnifyIcon" style="color:#fff"/>
          </span>
          <span class="icon is-right">
            <iconify-icon :icon="icons.closeIcon" style="color:#fff"/>
          </span>
        </p>
      </div>
    </div>
      <div v-for="recent in recents" :key="recent.id">
        <InboxMessage v-bind:recent="recent"/>
      </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Loading from '@/components/Loading'
import Avatar from '@/components/Avatar'
import IconifyIcon from '@iconify/vue';
import newChatIcon from '@iconify/icons-mdi/account-multiple-plus';
import newGroupIcon from '@iconify/icons-mdi/comment-plus';
import magnifyIcon from '@iconify/icons-mdi/magnify'
import closeIcon from '@iconify/icons-mdi/close'
import InboxMessage from './Inbox'

export default {
  name: 'Inbox',
  components: {
    Loading,
    Avatar,
    IconifyIcon,
    InboxMessage
  },
  data () {
    return {
      loading: false,
      icons: {
        newChatIcon: newChatIcon,
        newGroupIcon: newGroupIcon,
        magnifyIcon: magnifyIcon,
        closeIcon: closeIcon
      },
    }
  },
  computed: {
    ...mapState({
      messages: state => state.chat.messages,
      user: state => state.app.user,
      recents: state => state.chat.recents,
    })
  },
  watch: {
    recents (newVal) {
        console.log("RECIENTESSS",newVal)
    },
  },
  methods: {
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

.input{
    background-color: transparent !important;
    border-color: #fff !important;
    color: #fff !important;
}

::-webkit-input-placeholder { /* WebKit browsers */
    color:    red;
     opacity: 1 !important;
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
