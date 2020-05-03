<template>
  <div 
    ref="grid" 
    class="hex-grid"
    @click="onClick($event)">
  </div>
</template>

<script>
import { defineGrid, extendHex } from 'honeycomb-grid'
import { mapGetters, mapState } from 'vuex'
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
      selectedHex: null,
      oldPoint: null,
      wasUpdateOnClient: false
    }
  },
  created () {
    this.$store.dispatch("getAreas")
  },
  mounted () {
    this.draw = SVG(this.$refs.grid)
    this.grid = this.getGrid()
  },
  computed: {
    ...mapGetters(['currentState', 'occupedPoints']),
    ...mapState({
      // This is filled by WS message
      changeState: state => state.areas.changeState,
      currentArea: state => state.areas.currentArea,
      user: state => state.app.user
    }),
    Grid () {
      return defineGrid(this.getHex())
    },
  },
  methods: {
    onClick (e) {
      const {x, y} = this.getOffset(e)
      if (!this.isOverlaped([x,y])) {
        this.clearHex()
        this.selectCellByOffset(x, y, true)
        this.wasUpdateOnClient = true
      }
    },
    isOverlaped (point) {
      /*
        point: [Array[x,y]]
      */

      const obj = this.Grid.pointToHex(point)
      if (!this.occupedPoints) {
        return false
      }
      const results = 
                this.occupedPoints
                  .filter(point => point.x === obj.x 
                    && point.y === obj.y)

      const response = results.length ? true : false
      console.log(response)
      return response
    },
    selectCellByOffset(x, y, notify){
        const hexCoordinates = this.Grid.pointToHex([x, y])
        this.selectCellByCoordinates(hexCoordinates, notify)
    },
    selectCellByCoordinates(hexCoordinates, notify) {
      if (notify) {
        const message = {type:"grid.position", area: this.currentArea.id, x: hexCoordinates.x, y: hexCoordinates.y}
        this.$socket.send(JSON.stringify(message))
        this.oldPoint = hexCoordinates
      } 
      const selectedHex = this.grid.get(hexCoordinates)
      if (selectedHex) {
        selectedHex.filled()
        selectedHex.addImage()
        const neighbors = this.grid.neighborsOf(selectedHex)
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
      console.log(`clear hex ${this.oldPoint}`)
      const lastHex = this.grid.get(this.oldPoint)
      lastHex.clear()
    },
    onHover({ offsetX, offsetY }) {
        const hexCoordinates = this.Grid.pointToHex([offsetX, offsetY])
        const hex = this.grid.get(hexCoordinates)
        if (hex) {
          hex.highlight()
        }
    },
    paint () {
      const list = [[0,1], [2,2]]

      list.forEach(point => {
        const hex = this.grid.get(point)
        if (hex) {
          hex.filled()
          console.log(hex)
        }
      })
    },
    getGrid() {
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
    getHex() {
      const vm = this
      return extendHex({
        size: this.size,
        img: 'https://api.adorable.io/avatars/40/abott@adorable.png',
        render(draw) {
          const { x, y } = this.toPoint()
          const corners = this.corners()
          this.draw = draw
            .polygon(corners.map(({ x, y }) => `${x},${y}`))
            .fill('none')
            .stroke({width: this.border, color: 'rgba(224, 224, 224, .5)' })
            .translate(x, y)
        },

        highlight() {
          this.draw
            .stop(true, true)
            .fill({ opacity: 1, color: 'aquamarine' })
            .animate(1000)
            .fill({ opacity: 0, color: 'none' })
        },

        filled() {
          this.draw
            .stop(true, true)
            .stroke({width: 10, color: '#7f7fff' })
            .animate(1000)
            .stroke({width: 5, color: '#7f7fff' })
        },

        clear(){
          const position = this.toPoint()
          const centerPosition = this.center().add(position)
          this.draw
            .stop(true, true)
            // .stroke({width: 2, color: '#7f7fff' })
            // .animate(250)
            .stroke({width: 1, color: 'rgba(224, 224, 224, .5)' })
          
          // Draw a rect to clear the image
          vm.draw
            .rect(42,41)
            .fill('#f2f2f2')
            .move(centerPosition.x - 21, centerPosition.y - 21)
        },
        
        addImage() {
          const position = this.toPoint()
          const centerPosition = this.center().add(position)
          
          vm.draw
            .image(this.img)
            .translate(centerPosition.x - 20, centerPosition.y - 20)
        },

        addText() {
          const position = this.toPoint()
          const centerPosition = this.center().add(position)
          const fontSize = 12
          
          vm.draw
            .text(`${this.x},${this.y}`)
            .font({
              size: fontSize,
              anchor: 'middle',
              leading: 1.4,
              fill: 'black'
            })
            .translate(centerPosition.x, centerPosition.y - fontSize)
        }
      })
    },
    clearMassive(oldValues) {
      /* 
        oldValues: List of items from server
      */
      oldValues.forEach(old => {
        console.log(`clearing {old}`)
        let selectedHex = this.grid.get([old[0], old[1]])
        selectedHex.clear()
       }
      )
    }
  },
  watch: {
    size () {
      this.grid = this.getGrid()
    },
    currentState (value) {
      /* Executed when all state changed */ 
      console.log('currentState watcher')
      const vm = this
      value.forEach(userPosition => {
        const selectedHex = this.grid.get([userPosition.x, userPosition.y])
        if (selectedHex) {
          selectedHex.filled()
          selectedHex.addImage()
          if (userPosition.id === window.user_id) {
             vm.oldPoint = [userPosition.x, userPosition.y]
          }
        }
      })
    },
    changeState (value) {
      /* This is executed when a notification of user
        change is received */

      console.log('changeState Watcher')
      console.log(value)
      const point = [value.x, value.y]
      // Clear the old position
      // Se filtra porque los cambios hechos por nosotros mismos
      // se borran al hacer click
      if (!this.wasUpdateOnClient) {

        this.selectCellByCoordinates(point, false)
        console.log('Updating reading the message')

        if (window.user_id === value.user.id)
          this.oldPoint = point

        this.clearMassive(value.old)

      }

      this.wasUpdateOnClient = false
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
