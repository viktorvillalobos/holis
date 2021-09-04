<template>
  <div class="container">
    <div class="columns">
      <div class="column is-12">
        <p>Add new members to your workspace Adslad</p>
      </div>
    </div>
    <div class="columns">
      <div class="column is-12">
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="email" placeholder="myfriendsholis@gmail.com">
            <span class="icon is-small is-left material-icons-outlined">
              email
            </span>
            <span class="icon is-small is-right material-icons has-text-primary">
              delete
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="email" placeholder="myfriendsholis@gmail.com">
            <span class="icon is-small is-left material-icons-outlined">
              email
            </span>
            <span class="icon is-small is-right material-icons has-text-primary">
              delete
            </span>
          </p>
        </div>
        <button class="button is-fullwidth is-outlined is-primary">
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
export default {
  name: 'InvitationModal',
  data () {
    return {

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
</style>