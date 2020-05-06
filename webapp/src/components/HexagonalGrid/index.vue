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
  },
  async mounted () {
    this.draw = SVG(this.$refs.grid)
    this.grid = this.getGrid()

    await this.$store.dispatch("getAreas")
    this.loadInitialState()
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
        this.selectCellByOffset(x, y,this.user, true)
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
      const selectedHex = this.grid.get(hexCoordinates)
      if (selectedHex) {
        selectedHex.filled()
        selectedHex.addImage(user.avatar_thumb)
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
          
          vm.draw.circle(52).fill('#fdfdfd')
            .translate(centerPosition.x - 26, centerPosition.y - 26)
        },
        
        addImage(avatar) {
          const position = this.toPoint()
          const centerPosition = this.center().add(position)
          const img = vm.draw
            .image(avatar, 50, 50)

          vm.draw.circle(50)
            .attr({ fill:img})
            .translate(centerPosition.x - 25, centerPosition.y - 25)
            
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
    },
    loadInitialState () {
      console.log('currentState watcher')
      const vm = this
      this.currentState.forEach(userPosition => {
        const selectedHex = this.grid.get([userPosition.x, userPosition.y])
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
      this.grid = this.getGrid()
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
          this.clearMassive(value.old)
        }
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
