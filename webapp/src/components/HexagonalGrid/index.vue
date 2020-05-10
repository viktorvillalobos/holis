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
        selectedHex.filled()
        selectedHex.addImage(user.avatar_thumb)
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
    paint () {
      const list = [[0,1], [2,2]]

      list.forEach(point => {
        const hex = this.rectangle.get(point)
        if (hex) {
          hex.filled()
          console.log(hex)
        }
      })
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
    clearFromGrid(old) {
      /* 
        oldValues: List of items from server
      */
      console.log(`clearing {old}`)
      let selectedHex = this.rectangle.get([old[0], old[1]])
      selectedHex.clear()
    },
    async loadInitialState () {
      await this.$store.dispatch("getAreas")
      console.log('currentState watcher')
      const vm = this
      this.currentState.forEach(userPosition => {
        const selectedHex = this.rectangle.get([userPosition.x, userPosition.y])
        if (selectedHex) {
          selectedHex.filled()
          console.log('VALUE')
          console.log(userPosition)
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
    changeState (value) {
      /* This is executed when a notification of user
        change is received */
      const point = [value.x, value.y]
      // Clear the old position
      // Se filtra porque los cambios hechos por nosotros mismos
      // se borran al hacer click
      this.$store.commit('setOccupedStateChange', value.state)

      if (!this.wasUpdateOnClient) {
        console.log('No fue actualizado en este cliente')
        if (window.user_id === value.user.id)
        {
          this.oldPoint = point
        } else {
          this.selectCellByCoordinates(point, value.user, false)
          if (value.old)
            this.clearFromGrid(value.old)
        }
      }

      this.wasUpdateOnClient = false

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
//   height: 99vh;
   height: 1140px;
   width: 1140px;
  }

  svg {
    overflow: visible;
  }

  [id*="SvgjsImage"] {
    border-radius: 50%;
  }
</style>
