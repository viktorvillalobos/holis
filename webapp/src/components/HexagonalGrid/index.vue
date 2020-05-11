<template>
  <div 
    ref="grid" 
    class="hex-grid"
    @mouseover="onMouseOver($event)"
    @click="onClick($event)">
    <GridUserCard 
      :style="`top: ${hexTop}px; left: ${hexLeft}px`" 
      :name="hexOver && hexOver.user ? hexOver.user.name : null"
      :position="hexOver && hexOver.user ? hexOver.user.position : null"
      origin="bottom" 
      v-show="hexOver && hexOver.user"/>
  </div>
</template>

<script>
import { defineGrid } from 'honeycomb-grid'
import { mapGetters, mapState } from 'vuex'
import _ from 'lodash'
import  hex from './hex.js'
import  SVG  from 'svg.js'
import  GridUserCard  from '@/components/UserCard/GridUserCard'

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
      selectedHex: null,
      hexOver: null,
      hexTop: null,
      hexLeft: null
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
    this.hex =  hex.getHex(this.draw, this.size)
    this.Grid = defineGrid(this.hex)
    this.rectangle = this.getRectangle()

    await this.loadInitialState()
  },
  computed: {
    ...mapGetters(['currentState', 'occupedPoints']),
    ...mapState({
      // This is filled by WS message
      changeState: state => state.areas.changeState,
      deleteFromState: state => state.areas.deleteFromState,
      currentArea: state => state.areas.currentArea,
      user: state => state.app.user
    }),
  },
  methods: {
    onClick (e) {
      const {x, y} = this.getOffset(e)
      if (!this.isOverlaped([x,y])) {
        this.clearUserFromGrid(window.user_id)
        this.selectCellByOffset(x, y,this.user, true)
      }
    },
    isOverlaped (point) {
      const obj = this.Grid.pointToHex(point)
      const occuped = this.rectangle
                        .filter(hex => hex.x === obj.x && hex.y === obj.y && hex.user)
      console.log(occuped)
      return occuped.length !== 0
    },
    selectCellByOffset(x, y, user, notify){
        const hexCoordinates = this.Grid.pointToHex([x, y])
        this.selectCellByCoordinates(hexCoordinates, user, notify)
    },
    selectCellByCoordinates(hexCoordinates, user, notify) {
      if (notify) {
        const message = {type:"grid.position", area: this.currentArea.id, x: hexCoordinates.x, y: hexCoordinates.y}
        this.$socket.send(JSON.stringify(message))
      } 
      const selectedHex = this.rectangle.get(hexCoordinates)
      if (selectedHex) {
        selectedHex.filled(user)
        // const neighbors = this.rectangle.neighborsOf(selectedHex)
        // this.$emit('neighbors', neighbors)
      }
    },
    getOffset(e) {
      /* LayerX and LayerY Works well in chrome and firefox */ 
      const xpos = e.layerX
      const ypos = e.layerY
      return {x:xpos, y:ypos};
    },
    onMouseOver(e) {
        const {x, y} = this.getOffset(e)
        console.log(`mouse in x:${x} and y:${y}`)
        const hexCoordinates = this.Grid.pointToHex([x, y])
        const hex = this.rectangle.get(hexCoordinates)
        if (hex && hex.user ) {
          this.setHexOver(hex, x, y)
        } else {
          this.setHexOver(null, null, null)
        }
    },
    setHexOver: _.debounce(function(hex, x, y) {
        console.log('Hover User')
        console.log(hex)
        this.hexOver = hex
        this.hexLeft = x
        this.hexTop = y
    }, 400),
    getRectangle() {
      const vm = this
      this.draw.clear()
      return this.Grid.rectangle({
        width: 30,
        height: 30,
        // render each hex, passing the draw instance
        onCreate(hex) {
          hex.render(vm.draw)
        }
      })
    },
    clearOthersFromGrid() {
      
    },
    clearUserFromGrid(userId) {
      /* remove an user from grid 
        user: = user instance or userstat
        */
      console.log(`Clearing user id: ${userId} from grid`)
      this.rectangle
          .filter(x => x && x.user && x.user.id === userId)
          .forEach(x => x.clear())
    },
    clearFromGrid(oldPoint) {
      /* 
        oldPoint = [x,y]
      */
      console.log(`clearing {old}`)
      let selectedHex = this.rectangle.get(oldPoint)
      selectedHex.clear()
    },
    async loadInitialState () {
      await this.$store.dispatch("getAreas")
      this.currentState.forEach(userPosition => {
        const selectedHex = this.rectangle.get([userPosition.x, userPosition.y])
        if (selectedHex) {
          selectedHex.filled(userPosition)
        }
      })
    },
  },
  watch: {
    size () {
      this.rectangle = this.getRectangle()
    },
    changeState ({user, state}) {
      /* This is executed when a notification of user
        change is received */
      if (user.id  === window.user_id) return

      state
        .filter(x => x.id !== window.user_id)
        .forEach(userState => {
          const userPoint = [userState.x, userState.y]
          this.clearUserFromGrid(userState.id)
          this.selectCellByCoordinates(userPoint, userState, false)  
        })

    },
    deleteFromState({ user }) {
      // Remove user from state
      this.clearUserFromGrid(user.id)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  .hex-grid {
   // height: 99vh;
   width: 2500px;
   height: 2000px;
   overflow: auto;
  }

  svg {
    overflow: visible;
  }

  [id*="SvgjsImage"] {
    border-radius: 50%;
  }
</style>
