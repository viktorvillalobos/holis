<template>
  <div class="holis-config-notifications">
    <div class="header">
      <h3 class="header-title">
        <span class="material-icons header-icon has-text-primary">groups</span>
        Users
      </h3>
    </div>

    <div class="container">
      <div class="field mt-4">
        <p class="control has-icons-left has-icons-right">
          <input class="input" type="text" placeholder="Search for member" @input="debounceInput">
          <span class="icon is-left">
            <span class="material-icons">search</span>
          </span>
          <!--<span class="icon is-right" style="cursor: pointer;" v-if="query.length > 0">
            <span class="material-icons" style="color:#fff" >close</span>
          </span>-->
        </p>
      </div>

      <table class="table is-fullwidth">
        <thead>
          <tr>
            <th>Members:</th>
            <th>Is admin:</th>
          </tr>
        </thead>
        <tbody>
          <tr class="user-items" v-for="user in users" :key="user.id">
            <td>
              <div>
                <span class="icon-text">
                    <span class="icon is-rounded">
                        <img v-if="user.avatar_thumb" :src="user.avatar_thumb"/>
                        <font-awesome-icon v-else icon="user-circle" size="3x"/>
                    </span>
                    <div class="text-container">
                      <b class="header-new-chat-title">{{user.name.substring(0,50) || user.username.substring(0,50) }}</b>
                      <span class="email">
                        {{user.email}}
                      </span>
                    </div>
                </span>
              </div>
            </td>
            <td>Admin</td>
            <td>
              <div class="field">
                <input id="switchThinRoundedOutlinedDefault" type="checkbox" name="switchThinRoundedOutlinedDefault" class="switch is-thin is-rounded is-outlined" v-model="user.is_superuser">
              </div>
            </td>
            <td><span class="material-icons" style="color:#5D5FEF">delete</span></td>
          </tr>
        </tbody>
      </table>
      <button class="button is-primary" @click="handleInvitationModal">
        <span class="material-icons-outlined mr-2 is-size-6">
          person
        </span>
        Invite people
      </button>
    </div>
    
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'UsersRole',
  computed: {
    ...mapState({
      users: state => state.chat.users
    })
  },
  methods:{
    debounceInput: _.debounce(function (e) {
      //this.getInbox(e.target.value)
    }, 300),
    handleInvitationModal () {
      this.$store.commit('setInvitationModalActive')
    },
  },
  created(){
      this.$store.dispatch('getUsers', "")
  }
}
</script>

<style lang="scss" scoped>

th, td {
  border: none !important;
}

.user-items {

  td {
    vertical-align: middle;
    padding: 10px 15px !important;
  }
}

.user-items:hover {
  background-color: transparent;
}

.icon-text {
  align-items: center;

  .icon {
    padding: 0;
    height: 48px !important;
    width: 48px !important;
    overflow: hidden;
    border-radius: 50%;
  }

  .text-container {
    display: flex;
    max-width: calc(80% - 20px);
    margin-left: 20px;
    justify-content: space-around;
    flex-direction: column;

    .header-new-chat-title {
      width: 100%;
      margin: 0;
    }

    .email {
      font-size: 10px;
      line-height: 13px;
      color: #BDBDBD;
    }
  }
}
</style>
