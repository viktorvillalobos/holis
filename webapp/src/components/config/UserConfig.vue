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
            <label class="file-label">
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
  }),
  computed: {
    ...mapState({
      user: (state) => state.app.user,
    }),
  },
  created() {
    this.instance.avatar = this.user.avatar;
  },
};
</script>

<style lang="scss" scoped>
</style>