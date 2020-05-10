import {  extendHex } from 'honeycomb-grid'


function getHex (vmDraw, size) {
      return extendHex({
        size: size,
        user: null,
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

        filled(user) {
          this.user = user
          this.draw
            .stop(true, true)
            .stroke({width: 10, color: '#7f7fff' })
            .animate(1000)
            .stroke({width: 5, color: '#7f7fff' })

          this.addImage(user)
        },

        clear(){
          const position = this.toPoint()
          const centerPosition = this.center().add(position)
          this.draw
            .stop(true, true)
            // .stroke({width: 2, color: '#7f7fff' })
            // .animate(250)
            .stroke({width: 1, color: 'rgba(224, 224, 224, .5)' })
          
          vmDraw.circle(52).fill('#fdfdfd')
            .translate(centerPosition.x - 26, centerPosition.y - 26)
        },
        
        addImage(user) {
          const avatar = user.avatar || user.avatar_thumb
          const position = this.toPoint()
          const centerPosition = this.center().add(position)
          const img = vmDraw
            .image(avatar, 50, 50)

          vmDraw.circle(50)
            .attr({ fill:img})
            .translate(centerPosition.x - 25, centerPosition.y - 25)
            
        },

        addText() {
          const position = this.toPoint()
          const centerPosition = this.center().add(position)
          const fontSize = 12
          
          vmDraw
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

export default  {
  getHex
}
