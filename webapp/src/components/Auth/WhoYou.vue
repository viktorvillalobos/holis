<template>
  <div class="onboarding-whoyou">
    <ul class="onboarding-stepper">
      <li class="active">
        <span>1</span>¿Quién eres?
      </li>
      <li>
        <span>2</span>¿Cuál es tu equipo?
      </li>
      <li>
        <span>3</span>¡Invítalos!
      </li>
    </ul>
    <form @submit.prevent>
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
          <label class="label">Tu nombre</label>
        </div>
        <p class="control">
          <input
            @input="error = null"
            class="input"
            v-model="email"
            type="text"
            placeholder="Juanin Juan Harry"
          />
        </p>
      </div>
      <div class="field">
        <div class="field-label">
          <label class="label">Tu cargo</label>
        </div>
        <p class="control">
          <input
            @input="error = null"
            class="input"
            v-model="email"
            type="text"
            placeholder="Ej: Desarrollador, Diseñador, Domador de unicornios, etc."
          />
        </p>
      </div>
      <div class="field">
        <div class="field-label">
          <label class="label">Tu foto</label>
          <p>Muestrale a todos lo bien que te ves ;)</p>
        </div>
        <div class="control">
          <div class="file has-name">
            <label class="file-label">
              <input class="file-input" type="file" name="resume" />
              <span class="file-cta">
                <span class="file-icon">
                  <font-awesome-icon icon="upload" />
                </span>
                <span class="file-label">Choose a file…</span>
              </span>
              <span class="file-name">Screen Shot 2017-07-29 at 15.54.25.png</span>
            </label>
          </div>
        </div>
      </div>

      <div v-if="error" class="notification is-danger">
        <button @click="error = null" class="delete"></button>
        <p>{{ error }}</p>
      </div>
      <div class="auth-options">
        <Btn flat primary @btn-click="handleCreate">Inicia sesión</Btn>
        <Btn primary @btn-click="handleContinue">Continuar</Btn>
      </div>
    </form>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
export default {
  name: "WhoYou",
  components: {
    Btn
  },
  data() {
    return {
      error: "Esto es un error"
    };
  }
};
</script>
