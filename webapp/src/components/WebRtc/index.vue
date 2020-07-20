<template>
  <div class="video-list" v-show="enableVideo">
      <div v-for="item in videoList"
          v-bind:video="item"
          v-bind:key="item.id"
          class="video-item">
        <video
              controls
              autoplay
              playsinline
              ref="videos"
              :height="cameraHeight"
              :muted="item.muted"
              :id="item.id"/>
      </div>
  </div>
</template>

<script>
import apiClient from '../../services/api'
import RTCMultiConnection from '@/plugins/RTCMultiConnection'
import { mapState } from 'vuex'
import hark from 'hark'

require('adapterjs')
export default {
  name: 'vue-webrtc',
  components: {
    /* eslint-disable-next-line */
      RTCMultiConnection
  },
  props: {
    roomId: {
      type: String,
      default: 'public-room'
    },
    socketURL: {
      type: String,
      default: 'https://holis.chat:9001/'
    },
    cameraHeight: {
      type: [Number, String],
      default: 160
    },
    autoplay: {
      type: Boolean,
      default: true
    },
    screenshotFormat: {
      type: String,
      default: 'image/jpeg'
    },
    enableAudio: {
      type: Boolean,
      default: true
    },
    enableVideo: {
      type: Boolean,
      default: false
    },
    enableLogs: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      rtcmConnection: null,
      localVideo: null,
      videoList: [],
      canvas: null,
      streams: []
    }
  },
  computed: {
    ...mapState({
      muteAudio: state => state.webrtc.muteAudio,
      muteMicro: state => state.webrtc.muteMicro,
      connected: state => state.webrtc.connected,
    }),
    localStream () {
      if (!this.rtcmConnection || !this.rtcmConnection.streamEvents) return null

      return Object.values(this.rtcmConnection.streamEvents).filter(x => x.type === 'local')[0]
    }
  },
  watch: {
    connected (value) {
      console.log('Changing Connected Watcher in Office')
      if (value) {
        this.join()
      } else {
        this.streams = []
        this.leave()
      }
    },
    streams (value) {
      this.$store.dispatch('setStreamsCount', value.length + 1)
    },
    muteAudio (value) {
      this.videoList.forEach(video => {
        if (video !== this.localVideo) video.muted = value
      })
    },
    muteMicro (value) {
      this.muteMyMicro(value)
    }
  },
  async mounted () {
    var that = this
    this.rtcmConnection = new RTCMultiConnection()
    this.rtcmConnection.socketURL = this.socketURL
    this.rtcmConnection.userid = window.user_id

    const iceServers = await this.getIceServers()
    this.rtcmConnection.iceServers = iceServers
    this.rtcmConnection.autoCreateMediaElement = false
    this.rtcmConnection.enableLogs = this.enableLogs
    this.rtcmConnection.session = {
      audio: this.enableAudio,
      video: this.enableVideo
    }

    this.rtcmConnection.mediaConstraints = {
      audio: this.enableAudio,
      video: this.enableVideo
    }

    this.rtcmConnection.sdpConstraints.mandatory = {
      OfferToReceiveAudio: this.enableAudio,
      OfferToReceiveVideo: this.enableVideo
    }

    this.rtcmConnection.onstream = function (stream) {
      const found = that.videoList.find(video => {
        return video.id === stream.streamid
      })

      if (found === undefined) {
        let muted = false

        if (that.muteAudio) muted = true
        else muted = stream.type === 'local'

        const video = {
          id: stream.streamid,
          muted: muted
        }

        // This need to be unificated
        that.videoList.push(video)
        that.streams.push(stream)
      }

      setTimeout(function () {
        for (var i = 0, len = that.$refs.videos.length; i < len; i++) {
          if (that.$refs.videos[i].id === stream.streamid) {
            that.$refs.videos[i].srcObject = stream.stream
            break
          }
        }

        that.$emit('joined-room', {
          id: stream.streamid,
          isLocalUser: stream.streamid === that.localStream.streamid
        })
      }, 1000)

      that.initHark({
        stream: stream.stream,
        streamedObject: stream,
        connection: that.rtcmConnection
      })
    }
    this.rtcmConnection.onstreamended = function (stream) {
      var newList = []
      that.videoList.forEach(function (item) {
        if (item.id !== stream.streamid) {
          newList.push(item)
        }
      })
      that.videoList = newList
      that.$emit('left-room', {
        id: stream.streamid,
        isLocalUser: stream.streamid === that.localStream.streamid
      })
    }

    this.rtcmConnection.onspeaking = function (stream) {
      console.log('ON SPEAKING OUT')
      console.log(stream)
      that.$store.dispatch('userIsSpeaking', { userId: stream.userid, active: true })
    }

    this.rtcmConnection.onsilence = function (stream) {
      // e.streamid, e.userid, e.stream, etc.
      // e.mediaElement.style.border = ''
      console.log('ON SILENCE')
      console.log(stream)
      that.$store.dispatch('userIsSpeaking', { userId: stream.userid, active: false })
    }

    this.rtcmConnection.onvolumechange = function (event) {
      // event.mediaElement.style.borderWidth = event.volume
    }
  },
  methods: {
    initHark (args) {
      console.log('INIT HARK')
      const connection = args.connection
      const streamedObject = args.streamedObject
      const stream = args.stream

      const options = {}
      const speechEvents = hark(stream, options)

      speechEvents.on('speaking', function () {
        connection.onspeaking(streamedObject)
      })

      speechEvents.on('stopped_speaking', function () {
        connection.onsilence(streamedObject)
      })

      speechEvents.on('volume_change', function (volume, threshold) {
        streamedObject.volume = volume
        streamedObject.threshold = threshold
        connection.onvolumechange(streamedObject)
      })
    },
    async getIceServers () {
      const { data } = await apiClient.chat.getTurnCredentials()
      return data
    },
    muteMyMicro (mute) {
      this.localStream.stream.getAudioTracks()[0].enabled = !mute
    },
    join () {
      var that = this
      this.$store.commit('setStatusConnecting')
      this.rtcmConnection.openOrJoin(this.roomId, function (isRoomExist, roomid) {
        if (isRoomExist === false && that.rtcmConnection.isInitiator === true) {
          that.$emit('opened-room', roomid)
        }
        that.$store.commit('setStatusConnected')
      })
    },
    leave () {
      var that = this
      this.rtcmConnection.attachStreams.forEach(function (localStream) {
        localStream.stop()
        that.$store.commit('setStatusDisconnected')
      })
      this.videoList = []
    },
    capture () {
      return this.getCanvas().toDataURL(this.screenshotFormat)
    },
    getCanvas () {
      const video = this.getCurrentVideo()
      if (video !== null && !this.ctx) {
        const canvas = document.createElement('canvas')
        canvas.height = video.clientHeight
        canvas.width = video.clientWidth
        this.canvas = canvas
        this.ctx = canvas.getContext('2d')
      }
      const { ctx, canvas } = this
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      return canvas
    },
    getCurrentVideo () {
      if (this.localVideo === null) {
        return null
      }
      for (var i = 0, len = this.$refs.videos.length; i < len; i++) {
        if (this.$refs.videos[i].id === this.localVideo.id) { return this.$refs.videos[i] }
      }
      return null
    },
    shareScreen () {
      var that = this
      if (navigator.getDisplayMedia || navigator.mediaDevices.getDisplayMedia) {
        /* eslint-disable */
          function addStreamStopListener(stream, callback) {
            var streamEndedEvent = 'ended';
            if ('oninactive' in stream) {
                streamEndedEvent = 'inactive';
            }
            stream.addEventListener(streamEndedEvent, function() {
                callback();
                callback = function() {};
            }, false);
          }
          function onGettingSteam(stream) {
            that.rtcmConnection.addStream(stream);
            that.$emit('share-started', stream.streamid);
            addStreamStopListener(stream, function() {
              that.rtcmConnection.removeStream(stream.streamid);
              that.$emit('share-stopped', stream.streamid);
            });
          }
          function getDisplayMediaError(error) {
            console.log('Media error: ' + JSON.stringify(error));
          }
          if (navigator.mediaDevices.getDisplayMedia) {
            navigator.mediaDevices.getDisplayMedia({video: true, audio: false}).then(stream => {
              onGettingSteam(stream);
            }, getDisplayMediaError).catch(getDisplayMediaError);
          }
          else if (navigator.getDisplayMedia) {
            navigator.getDisplayMedia({video: true}).then(stream => {
              onGettingSteam(stream);
            }, getDisplayMediaError).catch(getDisplayMediaError);
          }
        }
      }
    }
  };
</script>
<style scoped>
  .video-list {
    background: whitesmoke;
    height: auto;
  }
    .video-list div {
      padding: 0px;
    }
  .video-item {
    background: #c5c4c4;
    display: inline-block;
  }
</style>
