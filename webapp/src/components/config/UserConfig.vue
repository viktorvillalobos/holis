<template>
  <div class="holis-config-user">
    <div class="columns">
      <div class="column is-3">
        <Avatar :img="instance.avatar" huge />
      </div>
      <div class="column">
        <div class="field">
          <label class="label" to="id_avatar">Tu foto</label>
          <div class="file has-name">
            <label class="file-label is-fullwidth">
              <input class="file-input" type="file" name="avatar" accept="image/*" id="id_avatar" />
              <span class="file-cta">
                <span class="file-icon">
                  <font-awesome-icon icon="upload" />
                </span>
                <span class="file-label">Choose a file</span>
              </span>
              <span id="fileName" class="file-name">Show off that nice smile you have!</span>
            </label>
          </div>
          <div class="field">
            <label class="label">Tu email</label>
            <input
              v-model="instance.email"
              class="input"
              type="email"
              placeholder="juaninjuanharry@mail.com"
              maxlength="50"
            />
          </div>
          <div class="field">
            <label class="label">Tu nombre</label>
            <input
              v-model="instance.name"
              class="input"
              type="text"
              placeholder="Juanin Juan Harry"
            />
          </div>
          <div class="field">
            <label class="label">Tu cargo</label>
            <input
              class="input"
              type="text"
              v-model="instance.position"
              placeholder="Ex. News producer, Studios\'s coordinator"
            />
          </div>
          <div class="field">
            <label class="label">Tu cumpleaños</label>
            <div class="columns">
              <div class="column">
                <div class="select is-fullwidth">
                  <select v-model="birthday[2]">
                    <option :value="null">Día</option>
                    <option v-for="N in 31" :key="N" :value="N < 9 ? '0' + N : N">{{N}}</option>
                  </select>
                </div>
              </div>
              <div class="column">
                <div class="select is-fullwidth">
                  <select v-model="birthday[1]">
                    <option :value="null">Mes</option>
                    <option
                      v-for="N in 12"
                      :key="N"
                      :value="N < 9 ? '0' + N : N"
                    >{{$moment().month(N - 1).format('MMMM')}}</option>
                  </select>
                </div>
              </div>
              <div class="column">
                <div class="select is-fullwidth">
                  <select v-model="birthday[0]">
                    <option :value="null">Año</option>
                    <option v-for="N in range()" :key="N" :value="N">{{N}}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="columns">
            <div class="column">
              <div
                v-if="toast.isActive"
                :class="['notification', {'is-danger' : toast.isError}, {'is-success' : !toast.isError}]"
              >
                <button @click="toast.isActive = false" class="delete"></button>
                <div class="toast-inner">
                  <img :src="toast.isError ? error : success" />
                  <div>
                    <h3>{{toast.title}}</h3>
                    {{toast.text}}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <ul class="card-actions">
            <li>
              <Btn @btn-click="handleSubmit" primary>Guardar</Btn>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import Avatar from "@/components/Avatar";
import Btn from "@/components/Btn";

import success from "@/assets/celebrate.svg";
import error from "@/assets/alert.svg";

export default {
  name: "userConfigs",
  components: {
    Avatar,
    Btn,
  },
  data: () => ({
    instance: {},
    min: null,
    birthday: [null, null, null],
    toast: {
      isError: false,
      isActive: false,
      title: "Yaaay!",
      text: "Everything's set up.",
    },
    success,
    error
  }),
  computed: {
    ...mapState({
      user: (state) => state.app.user,
    }),
  },
  created() {
    if (this.user) this.setInstance();
  },
  methods: {
    setInstance() {
      this.instance = this._.cloneDeep(this.user);
      if (this.instance.birthday) {
        this.birthday = this.instance.birthday.split("-");
      }
    },
    range() {
      let array = [],
        j = 0;
      const max = parseInt(this.$moment().format("YYYY")),
        min = parseInt(this.$moment().subtract(110, "years").format("YYYY"));
      for (var i = min; i <= max; i++) {
        array[j] = i;
        j++;
      }
      return array.reverse();
    },
    async handleSubmit() {
      this.instance.birthday = this.birthday.join("-");

      delete this.instance.avatar;

      try {
        await this.$store.dispatch("editUser", this.instance);
        this.toast = {
          isError: false,
          isActive: true,
          title: "Yaaay!",
          text: "Everything's set up.",
        };
      } catch (e) {
        this.toast = {
          isError: true,
          isActive: true,
          title: "Yikes!",
          text: "Something wnet wrong, please check your fields and try again.",
        };
      }
    },
  },
  watch: {
    user(val) {
      if (val) this.setInstance();
    },
  },
};
</script>

<style lang="scss" scoped>
.toast-inner {
  display: flex;
  align-items: center;

  img {
    margin-right: 15px;
  }

  h3 {
    font-weight: 600;
    font-size: 1.2rem;
  }
}
</style>