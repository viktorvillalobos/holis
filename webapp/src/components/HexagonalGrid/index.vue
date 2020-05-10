<template>
  <div 
    ref="grid" 
    class="hex-grid"
    @click="onClick($event)">
  </div>
</template>

<script>
import { defineGrid } from 'honeycomb-grid'
import { mapGetters, mapState } from 'vuex'
import  hex from './hex.js'
import  SVG  from 'svg.js'

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
  data () {
    return {
      draw: null,
      Grid: null,
      hex: null,
      selectedHex: null,
      oldPoint: null,
      wasUpdateOnClient: false
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
        this.clearHex()
        this.selectCellByOffset(x, y,this.user, true)
        this.wasUpdateOnClient = true
      }
    },
    isOverlaped (point) {
      // point: [Array[x,y]]

      const obj = this.Grid.pointToHex(point)
      if (!this.occupedPoints) {
        return false
      }
      const results = 
                this.occupedPoints
                  .filter(point => point.x === obj.x 
                    && point.y === obj.y)

      const response = results.length ? true : false
      console.log(`overlaped ${response}`)
      return response
    },
    selectCellByOffset(x, y, user, notify){
        const hexCoordinates = this.Grid.pointToHex([x, y])
        this.selectCellByCoordinates(hexCoordinates, user, notify)
    },
    selectCellByCoordinates(hexCoordinates, user, notify) {
      if (notify) {
        const message = {type:"grid.position", area: this.currentArea.id, x: hexCoordinates.x, y: hexCoordinates.y}
        this.$socket.send(JSON.stringify(message))
        this.oldPoint = hexCoordinates
      } 
      const selectedHex = this.rectangle.get(hexCoordinates)
      if (selectedHex) {
        selectedHex.filled(user)
        const neighbors = this.rectangle.neighborsOf(selectedHex)
        this.$emit('neighbors', neighbors)
      }
    },
    getOffset(e) {
      /* LayerX and LayerY Works well in chrome and firefox */ 
      const xpos = e.layerX
      const ypos = e.layerY
      return {x:xpos, y:ypos};
    },
    clearHex() {
      const lastHex = this.rectangle.get(this.oldPoint)
      lastHex.clear()
    },
    onHover({ offsetX, offsetY }) {
        const hexCoordinates = this.Grid.pointToHex([offsetX, offsetY])
        const hex = this.rectangle.get(hexCoordinates)
        if (hex) {
          hex.highlight()
        }
    },
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
      const vm = this
      this.currentState.forEach(userPosition => {
        const selectedHex = this.rectangle.get([userPosition.x, userPosition.y])
        if (selectedHex) {
          selectedHex.filled(userPosition)
          selectedHex.addImage(userPosition.avatar)
          if (userPosition.id === window.user_id) {
             vm.oldPoint = [userPosition.x, userPosition.y]
          }
        }
      })
    },
  },
  watch: {
    size () {
      this.rectangle = this.getRectangle()
    },
    changeState ({x, y, user, state}) {
      /* This is executed when a notification of user
        change is received */
      const point = [x, y]
      // Clear the old position
      // Se filtra porque los cambios hechos por nosotros mismos
      // se borran al hacer click

      /* if (window.user_id === user.id){
        this.oldPoint = point
      } else {
        this.selectCellByCoordinates(point, user, false)
        if (old)
          this.clearFromGrid(old)
      } */
      console.log(state)

      if (user.id === window.user_id) {
        this.oldPoint = point
      } else {
        state
          .filter(x => x.id !== window.user_id)
          .forEach(userState => {
            const userPoint = [userState.x, userState.y]
            this.clearUserFromGrid(userState.id)
            this.selectCellByCoordinates(userPoint, userState, false)  
          })
      }

      this.$store.commit('setOccupedStateChange', state)
    },
    deleteFromState(value) {
      // Remove user from state
      const point = [value.x, value.y]
      this.clearFromGrid(point)
      console.log(point)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  .hex-grid {
   height: 99vh;
  }

  svg {
    overflow: visible;
  }

  [id*="SvgjsImage"] {
    border-radius: 50%;
  }
</style>
