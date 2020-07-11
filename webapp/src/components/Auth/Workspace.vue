
<template>
  <form @submit.prevent>
    <h3>Inicia sesión en tu espacio de trabajo 👋</h3>
    <div class="field">
      <div class="field-label">
        <label class="label">Nombre de tu espacio de trabajo</label>
      </div>
      <p class="control">
        <input
          @input="error = null"
          v-model="workspaceName"
          class="input"
          type="text"
          placeholder="patacon-inc"
        />
      </p>
    </div>
    <div v-if="error" class="notification is-danger">
      <button @click="error = null" class="delete"></button>
      <p>{{ error }}</p>
    </div>
    <div class="auth-options">
      <Btn flat primary @btn-click="handleCreate">Crea un nuevo espacio de trabajo</Btn>
      <Btn primary @btn-click="handleContinue">Continuar</Btn>
    </div>
  </form>
</template>
<script>
import Btn from '@/components/Btn'
import { mapState } from 'vuex'

export default {
  name: 'Workspace',
  components: {
    Btn
  },
  data () {
    return {
      workspaceName: null,
      error: null
    }
  },
  computed: {
    ...mapState({
      currentCompany: state => state.auth.company
    })
  },
  methods: {
    handleCreate () {
      this.$router.push({ name: 'create-workspace' })
    },
    async handleContinue () {
      if (!this.workspaceName) {
        this.error = 'Debes ingresar el nombre de tu espacio de trabajo'
        return
      }
      await this.$store.dispatch('checkCompany', { companyName: this.workspaceName })

      if (!this.currentCompany) {
        this.error = 'Al parecer esta empresa aun no existe'
        return
      }
      this.$router.push({
        name: 'sign-in',
        params: { workspaceName: this.workspaceName }
      })
    }
  }
}
</script>
