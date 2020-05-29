<template>
  <div :class="['connect-user-card', {'connect-user-card--floats' : float}]">
    <div>
      <div class="connect-user-card-info">
        <Avatar :img="user ? user.avatar || user.avatar_thumb : null" />
        <div class="connect-user-card-info-text">
          <h3>{{user ? user.name : 'Nombre misterioso' }}</h3>
          <p>{{user ? user.position: 'Cargo misterioso'}}</p>
        </div>
      </div>
      <ul class="connect-user-card-options">
<!--        <li @click="emitVideo">
          <font-awesome-icon v-if="enableVideo" icon="video" />
          <font-awesome-icon v-else icon="video-slash" />
      </li> -->
        <li @click="emitSound">
          <font-awesome-icon v-if="!muteAudio" icon="volume-up" />
          <font-awesome-icon v-else icon="volume-mute" />
        </li>
        <li @click="emitMicro">
          <font-awesome-icon v-if="!muteMicro" icon="microphone-alt" />
          <font-awesome-icon v-else icon="microphone-alt-slash" />
        </li>
        <li @click="emitDisconnect">
          <font-awesome-icon v-if="connected" icon="phone" />
          <font-awesome-icon v-else icon="phone-slash" />
        </li>
        <li>
          <font-awesome-icon icon="sliders-h" />
        </li>
      </ul>
    </div>
    <div>
      <div :class="['dropdown', {'is-active' : stateMenuIsActive}]">
        <div class="dropdown-trigger">
          <button
            @click="stateMenuIsActive = !stateMenuIsActive"
            class="button"
            aria-haspopup="true"
            aria-controls="dropdown-menu2"
          >
            <span>{{userState}}</span>
            <span class="icon is-small">
              <font-awesome-icon icon="angle-down" />
            </span>
          </button>
        </div>
        <div class="dropdown-menu" id="dropdown-menu2" role="menu">
          <div class="dropdown-content">
            <div v-for="(state, index) in states" :key="state" @click="handleState(state)">
              <div class="dropdown-item">{{state}}</div>
              <hr v-if="index + 1 !== states.length" class="dropdown-divider" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import Avatar from "@/components/Avatar"

export default {
  name: "UserCard",
  props: {
    float: {
      type: Boolean
    },
    sound: {
      type: Boolean
    },
    micro: {
      type: Boolean
    },
    video: {
      type: Boolean
    },
    user: {
      type: Object
    }
  },
  components: {
    Avatar,
  },
  data() {
    return {
      stateMenuIsActive: false,
      states: [
        "💻 Disponible",
        "🤝 En reunión",
        "😋 En colación",
        "👻 Ausente"
      ],
      userState: null,
    };
  },
  computed: {
    ...mapState({
      muteAudio: state => state.webrtc.muteAudio,
      muteMicro: state => state.webrtc.muteMicro,
      enableVideo: state => state.webrtc.enableVideo,
      connected: state => state.webrtc.connected
    })
  },
  created() {
    this.userState = this.states[0];
  },
  methods: {
    emitSound() {
      this.$emit("sound");
      this.$store.commit("setMuteAudio")
    },
    emitVideo() {
      this.$store.dispatch("changeToVideo")
    },
    emitMicro() {
      console.log("emitMicro")
      this.$emit("micro");
      this.$store.commit("setMuteMicro")
    },
    emitDisconnect (){
      let value = !this.connected
      if (value) console.log("emitConnect")
      else console.log("emmitDisconnected")
      this.$store.commit("setConnected", value)
    },
    handleState(state) {
      this.userState = state;
      this.stateMenuIsActive = false;
    },
  }
};
</script>
<style lang="scss" scoped>
.connect-user-card {
  position: fixed;
  top: 7px;
  right: 341px;
  width: 326px;
  padding: 15px 8px 15px;
  transition: $aside-transition;
  box-shadow: $card-box-shadow;
  background: #fff;
  border-radius: $card-border-radius;

  > div {
    display: inline-flex;
    width: 100%;
    justify-content: space-between;
  }

  &-info {
    display: flex;
    align-items: center;
    justify-content: space-between;

    &-text {
      margin-left: 10px;
      h3 {
        font-size: 16px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 142px;
      }

      p {
        font-size: 12px;
      }
    }
  }

  &-options {
    display: inline-flex;

    li {
      margin-left: 10px;
      cursor: pointer;
    }
  }

  &--floats {
    right: 8px;
  }
}

.dropdown {
  width: 100%;

  &-trigger {
    width: 100%;
  }

  button {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }

  &.is-active {
    .dropdown-menu {
      width: 100%;

      .dropdown-item {
        &:hover {
          background: $light-gray;
          cursor: pointer;
        }
      }
    }
  }
}

.button {
  margin-top: 5px;
  background-color: $light-gray;
  border: 0;
  padding: 3px 10px;
  text-align: center;
  white-space: nowrap;
  height: 30px;
}

</style>
