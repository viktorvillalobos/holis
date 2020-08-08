<template>
  <div id="app">
    <webrtc
      :class="{'aside-expanded' : !float}"
      ref="webrtc"
      width="100%"
      :roomId="room"
      :enableAudio="enableAudio"
      :enableVideo="enableVideo"
      v-on:joined-room="joinedRoom"
      v-on:left-room="leftRoom"
      v-on:open-room="logEvent"
      v-on:share-started="logEvent"
      v-on:share-stopped="logEvent"
      @error="onError"
    />

    <router-view></router-view>
  </div>
</template>

<script>
import AOS from 'aos'
import 'aos/dist/aos.css'
import { mapState } from 'vuex'
import WebRTC from '@/components/WebRtc'

export default {
  name: "App",
  components: {
    webrtc: WebRTC
  },
  created () {
    this.$store.dispatch('getMe')
    AOS.init()
  },
  mounted () {
    this.$store.dispatch('connectNotificationsChannel', this)
    this.$store.dispatch('connectToGrid', { vm: this })
  },
  computed: {
    ...mapState({
      room: (state) => state.webrtc.room,
      muteAudio: (state) => state.webrtc.muteAudio,
      muteMicro: (state) => state.webrtc.muteMicro,
      enableAudio: (state) => state.webrtc.enableAudio,
      enableVideo: (state) => state.webrtc.enableVideo,
      float: (state) => state.app.isAsideRightActive,
    }),
  },
  methods: {
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
    },
    joinedRoom({ isLocalUser }) {
      console.log("An user is joined to room");
      if (!isLocalUser) {
        const audio = new Audio("/static/sounds/in.m4a");
        audio.play();
      }
    },
    leftRoom({ isLocalUser }) {
      console.log("An user left the room");
      if (!isLocalUser) {
        console.log("play left audio");
        const audio = new Audio("/static/sounds/out.m4a");
        audio.play();
      }
    },
  },
};
</script>

<style lang="scss">
input[type="range"] {
  -webkit-appearance: none;
  margin: 10px 0;
  width: 100%;
  &:focus {
    outline: none;
    &::-webkit-slider-runnable-track {
      background: #ccc;
    }
    &::-ms-fill-lower {
      background: $medium-gray;
    }
    &::-ms-fill-upper {
      background: $medium-gray;
    }
  }
  &::-webkit-slider-runnable-track {
    width: 100%;
    height: 8px;
    cursor: pointer;
    box-shadow: 0px 0px 0px #000000, 0px 0px 0px #0d0d0d;
    background: $medium-gray;
    border-radius: 25px;
    border: 0px solid #000101;
  }
  &::-webkit-slider-thumb {
    box-shadow: 0px 0px 0px #000000, 0px 0px 0px #0d0d0d;
    border: 1px solid $medium-gray;
    width: 18px;
    height: 18px;
    border-radius: 0;
    background: #fff;
    cursor: pointer;
    -webkit-appearance: none;
    margin-top: -3.6px;
  }
  &::-moz-range-track {
    width: 100%;
    height: 8px;
    cursor: pointer;
    animate: 0.2s;
    box-shadow: 0px 0px 0px #000000, 0px 0px 0px #0d0d0d;
    background: #ccc;
    border-radius: 25px;
    border: 0;
  }
  &::-moz-range-thumb {
    box-shadow: 0px 0px 0px #000000, 0px 0px 0px #0d0d0d;
    border: 0px solid #000000;
    height: 18px;
    width: 18px;
    border-radius: 7px;
    background: #fff;
    border: 1px solid $medium-gray;
    cursor: pointer;
  }
  &::-ms-track {
    width: 100%;
    height: 12.8px;
    cursor: pointer;
    animate: 0.2s;
    background: transparent;
    border-color: transparent;
    border-width: 39px 0;
    color: transparent;
  }
  &::-ms-fill-lower {
    background: $medium-gray;
    border: 0px solid #000101;
    border-radius: 50px;
    box-shadow: 0px 0px 0px #000000, 0px 0px 0px #0d0d0d;
  }
  &::-ms-fill-upper {
    background: $medium-gray;
    border: 0px solid #000101;
    border-radius: 50px;
    box-shadow: 0px 0px 0px #000000, 0px 0px 0px #0d0d0d;
  }
  &::-ms-thumb {
    box-shadow: 0px 0px 0px #000000, 0px 0px 0px #0d0d0d;
    border: 0px solid #000000;
    height: 18px;
    width: 18px;
    border-radius: 7px;
    background: #fff;
    border: 1px solid $medium-gray;
    cursor: pointer;
  }
}

@supports (-webkit-appearance: none) or (-moz-appearance: none) {
  input[type="checkbox"],
  input[type="radio"] {
    --active: #2f80ed;
    --active-inner: #fff;
    --focus: 2px rgba(39, 94, 254, 0.3);
    --border: #bbc1e1;
    --border-hover: #2f80ed;
    --background: #fff;
    --disabled: #f6f8ff;
    --disabled-inner: #e1e6f9;
    -webkit-appearance: none;
    -moz-appearance: none;
    height: 21px;
    outline: none;
    display: inline-block;
    vertical-align: top;
    position: relative;
    margin: 0;
    cursor: pointer;
    border: 1px solid var(--bc, var(--border));
    background: var(--b, var(--background));
    transition: background 0.3s, border-color 0.3s, box-shadow 0.2s;
    &:after {
      content: "";
      display: block;
      left: 0;
      top: 0;
      position: absolute;
      transition: transform var(--d-t, 0.3s) var(--d-t-e, ease),
        opacity var(--d-o, 0.2s);
    }
    &:checked {
      --b: var(--active);
      --bc: var(--active);
      --d-o: 0.3s;
      --d-t: 0.6s;
      --d-t-e: cubic-bezier(0.2, 0.85, 0.32, 1.2);
    }
    &:disabled {
      --b: var(--disabled);
      cursor: not-allowed;
      opacity: 0.9;
      &:checked {
        --b: var(--disabled-inner);
        --bc: var(--border);
      }
      & + label {
        cursor: not-allowed;
      }
    }
    &:hover {
      &:not(:checked) {
        &:not(:disabled) {
          --bc: var(--border-hover);
        }
      }
    }
    &:focus {
      box-shadow: 0 0 0 var(--focus);
    }
    &:not(.switch) {
      width: 21px;
      &:after {
        opacity: var(--o, 0);
      }
      &:checked {
        --o: 1;
      }
    }
    & + label {
      font-size: 14px;
      line-height: 21px;
      display: inline-block;
      vertical-align: top;
      cursor: pointer;
      margin-left: 4px;
    }
  }
  input[type="checkbox"] {
    &:not(.switch) {
      border-radius: 7px;
      &:after {
        width: 5px;
        height: 9px;
        border: 2px solid var(--active-inner);
        border-top: 0;
        border-left: 0;
        left: 7px;
        top: 4px;
        transform: rotate(var(--r, 20deg));
      }
      &:checked {
        --r: 43deg;
      }
    }
    &.switch {
      width: 38px;
      border-radius: 11px;
      &:after {
        left: 2px;
        top: 2px;
        border-radius: 50%;
        width: 15px;
        height: 15px;
        background: var(--ab, var(--border));
        transform: translateX(var(--x, 0));
      }
      &:checked {
        --ab: var(--active-inner);
        --x: 17px;
      }
      &:disabled {
        &:not(:checked) {
          &:after {
            opacity: 0.6;
          }
        }
      }
    }
  }
  input[type="radio"] {
    border-radius: 50%;
    &:after {
      width: 19px;
      height: 19px;
      border-radius: 50%;
      background: var(--active-inner);
      opacity: 0;
      transform: scale(var(--s, 0.7));
    }
    &:checked {
      --s: 0.5;
    }
  }
}

.field-switch {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.select {
  select {
    background-color: $light-gray !important;
  }
}

.select:not(.is-multiple):not(.is-loading)::after {
  border-color: $gray !important;
}
</style>
