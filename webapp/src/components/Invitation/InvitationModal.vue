<template>
  <div class="container">
    <div class="columns">
      <div class="column is-12">
        <p>Add new members to your workspace Adslad</p>
      </div>
    </div>
    <div class="columns">
      <div class="column is-12">
        <div v-for="(email, index) in emailList" :key="`email-${index}`" class="field">
          <p class="control has-icons-left has-icons-right">
            <span class="icon is-small is-left material-icons-outlined">
              email
            </span>
            <span 
              @click="deleteEmail(index)" 
              class="icon is-small is-right material-icons has-text-primary delete-icon" 
              v-if="emailList.length > 1"
            >
              delete
            </span>
            <input v-model="email.email" class="input" type="email" placeholder="myfriendsholis@gmail.com">
          </p>
        </div>
        <button class="button is-fullwidth is-outlined is-primary" @click="addEmail()">
          <span class="material-icons-outlined mr-3">
            add
          </span>
          Add new email
        </button>
      </div>
    </div>
    <div class="columns">
      <div class="column is-12">
        <p class="mb-4">
          <span class="material-icons-outlined rounded-icon mr-4 has-text-white">
            link
          </span>
          Share invitation link
        </p>
        <div class="field">
          <p class="control has-icons-right">
            <input class="input" type="text" placeholder="https://adslab.hol.is/app/invite">
            <span class="icon is-small is-right material-icons">
              copy
            </span>
          </p>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column is-12 has-text-centered">
        <button class="button is-outlined is-primary" @click="$emit('close')">
          Cancel
        </button>
        <button class="button is-primary ml-5">
          Invite
          <span class="material-icons-outlined ml-2 is-size-6">
            send
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: 'InvitationModal',
  data () {
    return {
      emailList: [
        {
          email: ''
        },
        {
          email: ''
        }
      ]
    }
  },
  methods: {
    addEmail () {
      this.emailList = [...this.emailList, {email: ''}]
    },
    deleteEmail (index) {
      this.emailList.splice(index, 1)
    },
    sendInvitations () {
      this.$store.dispatch('postInvitations', this.emailList)
    }
  }
}
</script>

<style lang="scss">
p {
  .rounded-icon {
    vertical-align: middle;
    background-color: #F63284;
    border-radius: 50%;
    padding: 5px;
    font-size: 20px;
  }
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #BDBDBD;

  .modal-header-title {
    font-size: 18px;
    font-weight: 500px;

    .modal-header-icon {
      vertical-align: middle;
      font-size: 20px;
      margin-right: 20px;
    }
  }
}

.icon {
  width: 45px !important;
  height: 40px !important;
  padding: 8px 10px;
}

.delete-icon {
  pointer-events: all !important;
  z-index: 99;
}

.delete-icon:hover {
  cursor: pointer;
}
</style>