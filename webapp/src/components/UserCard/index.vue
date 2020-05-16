<template>
  <div :class="['connect-user-card', {'connect-user-card--floats' : float}]">
    <div>
      <webrtc
        :class="{'aside-expanded' : !float}"
        ref="webrtc"
        width="100%"
        roomId="takata1234568979646665"
        :enableAudio="enableAudio"
        :enableVideo="enableVideo"
        v-on:joined-room="logEvent"
        v-on:left-room="logEvent"
        v-on:open-room="logEvent"
        v-on:share-started="logEvent"
        v-on:share-stopped="logEvent"
        @error="onError"
      />
      <div class="connect-user-card-info">
        <Avatar :img="user.avatar_thumb" />
        <div class="connect-user-card-info-text">
          <h3>{{user.name}}</h3>
          <p>{{user.position}}</p>
        </div>
      </div>
      <ul class="connect-user-card-options">
        <li @click="emitVideo">
          <font-awesome-icon v-if="video" icon="video" />
          <font-awesome-icon v-else icon="video-slash" />
        </li>
        <li @click="emitSound">
          <font-awesome-icon v-if="sound" icon="volume-up" />
          <font-awesome-icon v-else icon="volume-mute" />
        </li>
        <li @click="emitMicro">
          <font-awesome-icon v-if="micro" icon="microphone-alt" />
          <font-awesome-icon v-else icon="microphone-alt-slash" />
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
import Avatar from "@/components/Avatar";
import WebRTC from "@/components/WebRtc";

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
    webrtc: WebRTC
  },
  data() {
    return {
      stateMenuIsActive: false,
      states: [
        "💻 Disponible",
        " 🤝En reunión",
        "😋 En colación",
        "👻 Ausente"
      ],
      userState: null,
      enableAudio: true,
      enableVideo: false,
      muteMicro: false,
      muteAudio: false
    };
  },
  created() {
    this.userState = this.states[0];
  },
  methods: {
    emitSound() {
      this.$emit("sound");
    },
    emitVideo() {
      this.$emit("video");
    },
    emitMicro() {
      this.$emit("micro");
      this.connect = !this.connect;
      if (this.connect) this.$refs.webrtc.join();
      else this.$refs.webrtc.leave();
    },
    handleState(state) {
      this.userState = state;
      this.stateMenuIsActive = false;
    },
    logEvent(event) {
      console.log("Event : ", event);
    },
    onError(error, stream) {
      console.log("On Error Event", error, stream);
    },
    onCapture() {
      this.img = this.$refs.webrtc.capture();
    },
    onJoin() {
      console.log("Join to the connection");
    },
    onLeave() {
      this.$refs.webrtc.leave();
    },
    onShareScreen() {
      this.img = this.$refs.webrtc.shareScreen();
    }
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

.video-list {
  position: fixed;
  right: 70px;
  bottom: 18px;
  width: 220px;
  border-radius: 10px;
  transition: $aside-transition;

  &.aside-expanded {
    right: 400px;
  }
}
</style>
