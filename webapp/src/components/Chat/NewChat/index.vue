<template>
    <div>
        <div class="header-inbox p-5 columns">
            <button class="button is-ghost column is-1">
                <span class="icon is-small">
                    <span class="material-icons" style="color:#fff">chevron_left</span>
                </span>
            </button>
            <h3 class="column" style="color:#fff">Nuevo mensaje</h3>
        </div>
        <div class="field">
            <label class="label">Name</label>
            <div class="control">
                <input class="input is-primary" type="text" placeholder="Text input">
            </div>
        </div>
        <div class="field mr-5 ml-5 mt-5">
            <p class="control has-icons-left has-icons-right">
                <input class="input is-focused" type="email" placeholder="Search or start a new conversation">
                <span class="icon is-left">
                    <iconify-icon size="3x" :icon="icons.magnifyIcon" style="color:#fff"/>
                </span>
                <span class="icon is-right">
                    <iconify-icon :icon="icons.closeIcon" style="color:#fff"/>
                </span>
            </p>
        </div>
        <div class="user-items" v-for="user in users" :key="user.id">
            <span class="icon-text">
                <span class="icon">
                    <font-awesome-icon icon="user-circle" size="3x"/>
                </span>
                <span style="margin-left:20px">{{user.name || user.username}}</span>
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
  data () {
    return {
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
.header-inbox {
  font-family: $family-dm-sans;
  background: #364DFF;
  //background: linear-gradient(90deg, #364DFF 0%, #5165FF 100%);
  box-shadow: 0px 4px 4px rgba(224, 224, 224, 0.1);
}

.user-items{
    padding: 20px 40px 20px 40px;
}

.user-items:hover{
    cursor: pointer;
    background-color: rgba(128, 128, 128, 0.5);
}

/*.input{
    background-color: transparent !important;
    border-color: #ffffff !important;
    color: #ffffff !important;
}*/

//$input-placeholder-color: #fff;
</style>
