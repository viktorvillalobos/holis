
<template>
  <form @submit.prevent>
    <h3>Inicia sesión en {{$route.params.workspaceName}} 👋</h3>
    <div class="field">
      <div class="field-label">
        <label class="label">Tu email</label>
      </div>
      <p class="control">
        <input
          @input="error = null"
          class="input"
          v-model="email"
          type="mail"
          placeholder="mail@mail.com"
        />
      </p>
    </div>
    <div class="field">
      <div class="field-label">
        <label class="label">Tu contraseña</label>
      </div>
      <p class="control">
        <input
          @input="error = null"
          class="input"
          v-model="password"
          type="password"
          placeholder="*********"
        />
      </p>
      <router-link to>¿Olvidaste tu contraseña?</router-link>
    </div>
    <div v-if="error" class="notification is-danger">
      <button @click="error = null" class="delete"></button>
      <p>{{ error }}</p>
    </div>
    <div class="auth-options">
      <Btn flat primary @btn-click="handleBack">Volver</Btn>
      <Btn primary @btn-click="handleSignIn">Inicia sesión</Btn>
    </div>
  </form>
</template>
<script>
import Btn from "@/components/Btn";
export default {
  name: "Workspace",
  components: {
    Btn
  },
  data() {
    return {
      email: null,
      password: null,
      error: null
    };
  },
  methods: {
    handleBack() {
      this.$router.push({ name: "workspace" });
    },
    handleSignIn() {
      if (this.password && this.email) {
        this.$router.push({ name: "office" });
      } else {
        this.error = "Debes ingresar tu email y contraseña";
      }
    }
  }
};
</script>