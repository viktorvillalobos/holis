<template>
  <div class="holis-config-notifications">
    <div class="columns">
       <span class="material-icons-round column is-0" style="color: #5D6DE8">groups</span> 
       <p class="column ml-3 is-size-5" style="color: #333333">Invitations</p>
    </div>
    <div class="divider-test"></div>
    <p style="color: #333333" class="mt-4">Add new members to your workspace Adslad</p>

    <div class="mt-4" v-for="invitation in invitations" :key="invitation.email">
      <div class="field">
        <p class="control has-icons-left has-icons-right">
          <input class="input is-medium" type="email" :value="invitation.email" placeholder="myfriendholis@gmail.com">
          <span class="icon is-small is-left">
            <span class="material-icons-round" style="color: #BDBDBD">mail_outline</span>
          </span>
          <span class="icon is-small is-right is-clickeable" @click.prevent="newInvitation">
            <span class="material-icons-round" style="color: #5D5FEF">delete</span>
          </span>
        </p>
      </div>
    </div>

    <button class="button is-primary is-outlined is-medium is-fullwidth mt-4" @click="newInvitation">
      <span class="icon is-small">
        <span class="material-icons-round">
          add
        </span>
      </span>
      <span>Add new email</span>
    </button>

    <div class="mt-4">
      <span class="material-icons-round" style="color: #F63284">link</span> <b>Share invitation link</b>
    </div>
    <div class="field mt-4">
      <p class="control has-icons-left has-icons-right">
        <input class="input is-medium" type="email" placeholder="myfriendholis@gmail.com">
        <span class="icon is-small is-left">
          <span class="material-icons-round" style="color: #BDBDBD">mail_outline</span>
        </span>
        <span class="icon is-small is-right">
          <span class="material-icons-round" style="color: #5D5FEF">content_copy</span>
        </span>
      </p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Invitations',
  data () {
    return {
      invitations: []
    }
  },
  methods:{
    newInvitation() {
      this.invitations.push({email: ""})
    }
  },
  created(){
    this.newInvitation()
  }
}
</script>

<style lang="scss" scoped>
</style>
