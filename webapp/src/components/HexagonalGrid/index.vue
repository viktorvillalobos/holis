<template>
  <div>
    <div
      id="grid"
      ref="grid"
      class="hex-grid"
      @mouseover="onMouseOver($event)"
      @click="onClick($event)">

    </div>
        <GridUserCard
          :style="`top: ${hexTop}px; left: ${hexLeft}px`"
          :isLocalUser="hexOver ? hexOver.isLocalUser : false"
          :name="hexOver && hexOver.user ? hexOver.user.name : 'Secret Name'"
          :user="hexOver && hexOver.user ? hexOver.user : null"
          :position="hexOver && hexOver.user ? hexOver.user.position : 'Cargo no definido'"
          :status="userCurrentState"
          :img="hexOver && hexOver.user ? hexOver.user.avatar || hexOver.user.avatar_thumb : null"
          :origin="overOrigin"
          @onMouseOver="onGridUserCardOver(true)"
          @onMouseLeave="onGridUserCardOver(false)"
          @onChat="onChat"
          v-if="hexOver && hexOver.user"/>
  </div>
</template>

<script>
import { defineGrid } from 'honeycomb-grid'
import { mapGetters, mapState } from 'vuex'
import _ from 'lodash'
import hex from './hex.js'
import SVG from 'svg.js'
import GridUserCard from '@/components/UserCard/GridUserCard'
import TouchScroll from '@/plugins/touchScroll/TouchScroll'

export default {
  name: 'HexGrid',
  props: {
    size: {
      type: Number,
      default: 50
    },
    border: {
      type: Number,
      default: 1
    }
  },
  components: {
    GridUserCard
  },
  data () {
    return {
      draw: null,
      Grid: null,
      hex: null,
      hexOver: null,
      hexTop: null,
      hexLeft: null,
      isFirefox: false,
      overOrigin: 'bottom',
      room: null,
      localUserHex: null,
      neighbors: null,
      gridOver: false
    }
  },
  async mounted () {
    this.initGrid()
    this.isFirefox = window.navigator.userAgent.toLowerCase().indexOf('firefox') > -1
    this.setScroll()
    this.$store.dispatch('connectToGrid', { vm: this })

    await this.loadInitialState()

    /* eslint-disable-next-line */
    window.clearInterval(window.refreshStatusInterval)

    window.refreshStatusInterval = setInterval(async () => {
      console.log(`Refreshing State ${new Date()}`)
      await this.loadInitialState()
    }, 30000)
  },
  computed: {
    ...mapGetters(['currentState', 'occupedPoints']),
    ...mapState({
      // This is filled by WS message
      changeState: state => state.areas.changeState,
      changeStatus: state => state.areas.changeStatus,
      deleteFromState: state => state.areas.deleteFromState,
      currentArea: state => state.areas.currentArea,
      user: state => state.app.user,
      connected: state => state.webrtc.connected,
      disconnectByControl: state => state.webrtc.disconnectByControl,
      userSpeaking: state => state.webrtc.userSpeaking
    }),
    userCurrentState () {
      return this.hexOver && this.hexOver.user ? this.hexOver.user.statuses.filter(status => status.is_active)[0] : 'Working'
    }
  },
  methods: {
    onChat (user) {
      console.log(`Opening a chat with ${user.name}`)
      this.$store.commit('setAsideRightActive')
      this.$store.commit('setCurrentChatName', user.name || user.username)
      this.$store.commit('setCurrentChatJID', user.jid)
      this.$store.dispatch('getMessages', user.jid)
    },
    initGrid () {
      /*
        Grid Creation

        draw = SVG.JS Library Draw object, can be replaced by PixiJS.
        hex = HoneyCombJS ExtendHex, define a HEX object.
        Grid = is a grid object factory, used to define grids.
        rectangle = is a like rectangle grid defined by the Grid
      */
      this.draw = SVG(this.$refs.grid)
      this.hex = hex.getHex(this.draw, this.size)
      this.Grid = defineGrid(this.hex)
      this.rectangle = this.getRectangle()
    },
    onClick (e) {
      const { x, y } = this.getOffset(e)
      if (!this.isOverlaped([x, y])) {
        this.clearUserFromGrid(window.user_id)
        this.selectCellByOffset(x, y, this.user, true)
      }
    },
    isOverlaped (point) {
      const obj = this.Grid.pointToHex(point)
      const occuped = this.rectangle
        .filter(hex => hex.x === obj.x && hex.y === obj.y && hex.user)
      return occuped.length !== 0
    },
    selectCellByOffset (x, y, user, isLocalUser) {
      const hexCoordinates = this.Grid.pointToHex([x, y])
      this.selectCellByCoordinates(hexCoordinates, user, isLocalUser)
    },
    selectCellByCoordinates (hexCoordinates, user, isLocalUser) {
      const selectedHex = this.rectangle.get(hexCoordinates)
      if (selectedHex) {
        selectedHex.filled(user, isLocalUser)
        if (isLocalUser) {
          this.setNeighbors(selectedHex)
          this.connectToWebRTC(selectedHex)
          this.sendChangePositionNotification(hexCoordinates)
        }
      }
    },
    setNeighbors (selectedHex) {
      this.neighbors = this.rectangle
        .neighborsOf(selectedHex)
        .filter(hex => hex.user !== null)
    },
    connectToWebRTC (selectedHex) {
      // Solo si es el usuario actual
      this.localUserHex = selectedHex
      this.$store.commit('setCurrentUserHex')
      if (this.neighbors.length) {
        this.room = this.neighbors[0].user.room
        console.log(`Connectiong to ${this.room} channel`)
      } else {
        this.room = this.uuidv4()
        console.log(`Creating new channel ${this.room} channel`)
      }
      this.$store.dispatch('disconnectAndConnect', this.room)
    },
    sendChangePositionNotification (hexCoordinates) {
      const message = {
        type: 'grid.position',
        area: this.currentArea.id,
        x: hexCoordinates.x,
        y: hexCoordinates.y,
        room: this.room
      }

      window.$socketGrid.sendObj(message)
    },
    getOffset (e) {
      /* LayerX and LayerY Works well in chrome and firefox */
      if (this.isFirefox) { return { x: e.layerX, y: e.layerY } } else { return { x: e.offsetX, y: e.offsetY } }
    },
    onGridUserCardOver (active) {
      this.gridOver = active
    },
    onMouseOver (e) {
      const { x, y } = this.getOffset(e)
      const hexCoordinates = this.Grid.pointToHex([x, y])
      const hex = this.rectangle.get(hexCoordinates)
      if (hex && hex.user) {
        this.setHexOverPosition(hex, x, y)
      } else {
        this.clearHexOver()
      }
    },
    clearHexOver () {
      if (!this.gridOver) {
        this.hexOver = null
        this.hexLeft = 0
        this.hexTop = 0
      }
    },
    setHexOverPosition: _.debounce(function (hex, x, y) {
      /*
        setHexOverPosition
        Set the position in x and y to the UserHoverGrid
        depends of the offsetX and offsetY
      */
      this.hexOver = hex
      const maxWidth = window.innerWidth - 300
      const maxHeight = window.innerHeight - 150
      this.overOrigin = 'bottom'

      if (x > maxWidth) x = x - 300
      if (y > maxHeight) y = y - 150

      this.hexLeft = x
      this.hexTop = y
    }, 400),
    getRectangle () {
      const vm = this
      this.draw.clear()
      return this.Grid.rectangle({
        width: 30,
        height: 30,
        // render each hex, passing the draw instance
        onCreate (hex) {
          hex.render(vm.draw)
        }
      })
    },
    clearUserFromGrid (userId) {
      /* remove an user from grid
        user: = user instance or userstat
        */
      console.log(`Clear user # ${userId}`)
      this.rectangle
        .filter(x => x && x.user && x.user.id === userId)
        .forEach(x => x.clear())
    },
    clearFromGrid (oldPoint) {
      /*
        oldPoint = [x,y]
      */
      const selectedHex = this.rectangle.get(oldPoint)
      selectedHex.clear()
    },
    async loadInitialState () {
      await this.$store.dispatch('getAreas')
      this.paintAllState()
    },
    clearAllState () {
      this.rectangle.filter(x => x.user).forEach(x => x.clear())
    },
    paintAllState () {
      this.currentState.forEach(userPosition => {
        // Verificar que no esta aquí, puede ser que se haya bugueado.
        const exists = this.rectangle.filter(x => x.user && x.user.id === userPosition.id)[0]

        // Fill
        const selectedHex = this.rectangle.get([userPosition.x, userPosition.y])

        if (!exists && selectedHex) {
          selectedHex.filled(userPosition)
        }

        if (exists && selectedHex && ((exists.x !== selectedHex.x) || (exists.y !== selectedHex.y))) {
          exists.clear()
          selectedHex.filled(userPosition)
        }
      })
    },
    setScroll () {
      this.draw.node.setAttribute('width', '2000px')
      this.draw.node.setAttribute('height', '1700px')
      const viewer = new TouchScroll()
      viewer.init({
        id: 'grid',
        draggable: true,
        wait: false
      })
    },
    uuidv4 () {
      return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
      )
    }
  },
  watch: {
    userSpeaking: {
      handler (value) {
        const hex = this.rectangle.filter(x => x.user && x.user.id === value.userId)[0]
        value.active ? hex.animateVoice() : hex.clearVoiceAnimation()
      },
      deep: true
    },
    connected (value) {
      if (!value && this.disconnectByControl) this.localUserHex.clear()
    },
    size () {
      this.rectangle = this.getRectangle()
    },
    changeStatus ({ user, status }) {
      const hex = this.rectangle.filter(hex => hex.user && hex.user.id === user.id)[0]
      hex.clearStatus()
      hex.addStatus(status)
    },
    changeState ({ user, state }) {
      /* This is executed when a notification of user
        change is received */
      const isLocalUser = user.id === window.user_id

      if (isLocalUser) {
        this.$store.dispatch('setCurrentState', state)
        return
      }
      state
        .filter(x => x.id !== window.user_id)
        .forEach(userState => {
          const userPoint = [userState.x, userState.y]
          this.clearUserFromGrid(userState.id)
          this.selectCellByCoordinates(userPoint, userState, false)
        })

      this.$store.dispatch('setCurrentState', state)
    },
    deleteFromState ({ user, state }) {
      // Remove user from state
      console.log('DELETE FROM STATE')
      console.log(user)
      console.log(state)
      this.clearUserFromGrid(user.id)
      this.$store.dispatch('setCurrentState', state)

      if (user.id === window.user_id) {
        this.$store.commit('disconnectByControl')
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  body {
    overflow: hidden;
  }

  .hex-grid {
     height: 99vh;
     overflow: hidden;
  }

  svg {
    overflow: visible;
  }

  [id*="SvgjsImage"] {
    border-radius: 50%;
  }
</style>
