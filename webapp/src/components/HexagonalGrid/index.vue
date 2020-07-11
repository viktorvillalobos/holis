<template>
  <div
    id="grid"
    ref="grid"
    class="hex-grid"
    @mouseover="onMouseOver($event)"
    @click="onClick($event)">

    <GridUserCard
      :style="`top: ${hexTop}px; left: ${hexLeft}px`"
      :name="hexOver && hexOver.user ? hexOver.user.name : 'Secret Name'"
      :position="hexOver && hexOver.user ? hexOver.user.position : 'Cargo no definido'"
      :img="hexOver && hexOver.user ? hexOver.user.avatar || hexOver.user.avatar_thumb : null"
      :origin="overOrigin"
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
      localUserHex: null
    }
  },
  async mounted () {
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

    this.isFirefox = window.navigator.userAgent.toLowerCase().indexOf('firefox') > -1
    this.setScroll()

    await this.loadInitialState()
  },
  computed: {
    ...mapGetters(['currentState', 'occupedPoints']),
    ...mapState({
      // This is filled by WS message
      changeState: state => state.areas.changeState,
      deleteFromState: state => state.areas.deleteFromState,
      currentArea: state => state.areas.currentArea,
      user: state => state.app.user,
      connected: state => state.webrtc.connected,
      disconnectByControl: state => state.webrtc.disconnectByControl
    })
  },
  methods: {
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
        selectedHex.filled(user)
        const neighbors = this.rectangle
          .neighborsOf(selectedHex)
          .filter(hex => hex.user !== null)

        if (isLocalUser) {
          // Solo si es el usuario actual
          this.localUserHex = selectedHex
          this.$store.commit('setCurrentUserHex')
          if (neighbors.length) {
            this.room = neighbors[0].user.room
            console.log(`Connectiong to ${this.room} channel`)
          } else {
            this.room = this.uuidv4()
            console.log(`Creating new channel ${this.room} channel`)
          }
          this.$store.dispatch('disconnectAndConnect', this.room)
        }
      }

      if (isLocalUser) {
        const message = {
          type: 'grid.position',
          area: this.currentArea.id,
          x: hexCoordinates.x,
          y: hexCoordinates.y,
          room: this.room
        }

        this.$socket.send(JSON.stringify(message))
      }
    },
    getOffset (e) {
      /* LayerX and LayerY Works well in chrome and firefox */
      if (this.isFirefox) { return { x: e.layerX, y: e.layerY } } else { return { x: e.offsetX, y: e.offsetY } }
    },
    onMouseOver (e) {
      const { x, y } = this.getOffset(e)
      const hexCoordinates = this.Grid.pointToHex([x, y])
      const hex = this.rectangle.get(hexCoordinates)
      if (hex && hex.user) {
        this.setHexOverPosition(hex, x, y)
      } else {
        this.setHexOverPosition(null, null, null)
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
    clearOthersFromGrid () {

    },
    clearUserFromGrid (userId) {
      /* remove an user from grid
        user: = user instance or userstat
        */
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
      this.currentState.forEach(userPosition => {
        const selectedHex = this.rectangle.get([userPosition.x, userPosition.y])
        if (selectedHex) {
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
    connected (value) {
      if (!value && this.disconnectByControl) this.localUserHex.clear()
    },
    size () {
      this.rectangle = this.getRectangle()
    },
    changeState ({ user, state }) {
      /* This is executed when a notification of user
        change is received */
      if (user.id === window.user_id) {
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
      this.clearUserFromGrid(user.id)
      this.$store.dispatch('setCurrentState', state)
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
