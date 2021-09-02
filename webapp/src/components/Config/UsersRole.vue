<template>
  <div class="holis-config-notifications">
    <div class="columns">
       <span class="material-icons-round column is-0" style="color: #5D6DE8">groups</span> 
       <p class="column ml-3 is-size-5" style="color: #333333">Users and Role</p>
    </div>
    <div class="divider-test"></div>

    <div class="field mt-4">
      <p class="control has-icons-left has-icons-right">
        <input class="input input-inbox" placeholder="Search person or group" @input="debounceInput">
        <span class="icon is-left">
          <span class="material-icons" style="color:#fff">search</span>
        </span>
        <!--<span class="icon is-right" style="cursor: pointer;" v-if="query.length > 0">
          <span class="material-icons" style="color:#fff" >close</span>
        </span>-->
      </p>
    </div>

    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th>Member List</th>
          <th>Role</th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr class="user-items" v-for="user in users" :key="user.id">
          <th>
            <div>
                <span class="icon-text">
                    <span class="icon">
                        <Avatar v-if="user.avatar_thumb" :img="user.avatar_thumb"/>
                        <font-awesome-icon v-else icon="user-circle" size="3x"/>
                    </span>
                    <b class="header-new-chat-title">{{user.name.substring(0,50) || user.username.substring(0,50) }}</b>
                </span>
            </div>
          </th>
          <td>Admin</td>
          <td>23</td>
          <td><span class="material-icons" style="color:#5D5FEF">delete</span></td>
          <td><span class="material-icons" style="color:#666C78">edit</span></td>
        </tr>
      </tbody>
    </table>
    
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
  },
  created(){
      this.$store.dispatch('getUsers', "")
  }
}
</script>

<style lang="scss" scoped>
</style>
