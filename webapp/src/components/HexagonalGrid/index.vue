<template>
  <div 
    ref="grid" 
    class="hex-grid"
    @click="onClick($event)">
  </div>
</template>

<script>
import { defineGrid, extendHex } from 'honeycomb-grid'
import { mapGetters } from 'vuex'
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
      selectedHex: null
    }
  },
  mounted () {
    this.draw = SVG(this.$refs.grid)
    this.grid = this.getGrid()
  },
  computed: {
    ...mapGetters(['currentState']),
    Grid () {
      return defineGrid(this.hex)
    },
    hex() {
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
            .stroke({width: 2, color: '#7f7fff' })
            .animate(250)
            .stroke({width: 1, color: 'rgba(224, 224, 224, .5)' })
          
          // Draw a rect to clear the image
          vm.draw
            .rect(42,40)
            .fill('#f2f2f2')
            .move(centerPosition.x - 21, centerPosition.y - 20)
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
    }
  },
  methods: {
    onClick (e) {
        const {x, y} = this.getOffset(e)
        this.clearHex()
        this.selectCellByOffset(x, y)
    },
    selectCellByOffset(x, y){
        const hexCoordinates = this.Grid.pointToHex([x, y])
        this.selectCellByCoordinates(hexCoordinates)
    },
    selectCellByCoordinates(hexCoordinates) {
        this.selectedHex = this.grid.get(hexCoordinates)
        if (this.selectedHex) {
          this.selectedHex.filled()
          this.selectedHex.addImage()
          const neighbors = this.grid.neighborsOf(this.selectedHex)
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
      if (this.selectedHex)
        this.selectedHex.clear()
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
  },
  watch: {
    size () {
      this.grid = this.getGrid()
    },
    currentState (value) {
      value.forEach(userPosition => {
        this.selectCellByCoordinates([userPosition.x, userPosition.y])
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  .hex-grid {
   height: 100vh;
  }

  svg {
    overflow: visible;
  }

  [id*="SvgjsImage"] {
    border-radius: 50%;
  }
</style>
