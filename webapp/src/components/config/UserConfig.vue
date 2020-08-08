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
            <input class="input" type="email" placeholder="juaninjuanharry@mail.com" maxlength="50" />
          </div>
          <div class="field">
            <label class="label">Tu nombre</label>
            <input class="input" type="text" placeholder="Juanin Juan Harry" />
          </div>
          <div class="field">
            <label class="label">Tu cargo</label>
            <input class="input" type="text" placeholder="Juanin Juan Harry" />
          </div>
          <div class="field">
            <label class="label">Tu cumpleaños</label>
            <div class="columns">
              <div class="column">
                <div class="select is-fullwidth">
                  <select>
                    <option>Día</option>
                    <option v-for="N in 31" :key="N">{{N}}</option>
                  </select>
                </div>
              </div>
              <div class="column">
                <div class="select is-fullwidth">
                  <select>
                    <option>Mes</option>
                    <option v-for="N in 12" :key="N">{{$moment().month(N).format('MMMM')}}</option>
                  </select>
                </div>
              </div>
              <div class="column">
                <div class="select is-fullwidth">
                  <select>
                    <option>Año</option>
                    <option v-for="N in range()" :key="N">{{N}}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <ul class="card-actions">
            <li>
              <Btn primary>Guardar</Btn>
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

export default {
  name: "userConfigs",
  components: {
    Avatar,
    Btn,
  },
  data: () => ({
    instance: {},
    min: null,
  }),
  computed: {
    ...mapState({
      user: (state) => state.app.user,
    }),
  },
  created() {
    this.instance.avatar = this.user.avatar;
  },
  methods: {
    range() {
      let array = [],
        j = 0;
      const max = parseInt(this.$moment().subtract(10, "years").format("YYYY")),
        min = parseInt(this.$moment().subtract(110, "years").format("YYYY"));
      for (var i = min; i <= max; i++) {
        array[j] = i;
        j++;
        console.log(i);
      }
      return array.reverse();
    },
  },
};
</script>

<style lang="scss" scoped>
</style>