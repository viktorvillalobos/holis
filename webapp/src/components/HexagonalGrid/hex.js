import { extendHex } from 'honeycomb-grid'

function getHex (vmDraw, size) {
  return extendHex({
    size: size,
    user: null,
    image: null,
    status: null,
    render (draw) {
      const { x, y } = this.toPoint()
      const corners = this.corners()
      this.draw = draw
        .polygon(corners.map(({ x, y }) => `${x},${y}`))
        .fill('none')
        .stroke({ width: this.border, color: 'rgba(224, 224, 224, .5)' })
        .translate(x, y)
    },

    highlight () {
      this.draw
        .stop(true, true)
        .fill({ opacity: 1, color: 'aquamarine' })
        .animate(1000)
        .fill({ opacity: 0, color: 'none' })
    },

    filled (user) {
      this.user = user
      this.draw
        .stop(true, true)
        // .stroke({ width: 10, color: '#7f7fff' })
        // .animate(1000)
        .stroke({ width: 5, color: '#7f7fff' })

      this.addImage(user)
      this.addStatus()
    },

    clear () {
      this.user = null
      this.clearImage()
      this.clearStatus()
      this.draw
        .stop(true, true)
        .stroke({ width: 1, color: 'rgba(224, 224, 224, .5)' })
    },
    clearImage () {
      this.image.node.remove()
    },

    addImage (user, fill) {
      console.log('Adding image')
      console.log(fill)
      const avatar = user.avatar || user.avatar_thumb
      const position = this.toPoint()
      const centerPosition = this.center().add(position)
      const img = vmDraw
        .image(avatar, 50, 50)
      fill = fill || img

      this.image = vmDraw.circle(50)
        .attr({ fill })
        .translate(centerPosition.x - 25, centerPosition.y - 25)
    },

    addText () {
      const position = this.toPoint()
      const centerPosition = this.center().add(position)
      const fontSize = 12

      this.text = vmDraw
        .text(`${this.x},${this.y}`)
        .font({
          size: fontSize,
          anchor: 'middle',
          leading: 1.4,
          fill: 'black'
        })
        .translate(centerPosition.x, centerPosition.y - fontSize)
    },
    clearStatus () {
      if (this.status) this.status.node.remove()
    },
    addStatus () {
      const position = this.toPoint()
      const centerPosition = this.center().add(position)
      const fontSize = 16
      if (this.user) {
        const status = this.user.statuses.filter(x => x.is_active)[0]
        if (status) {
          this.status = vmDraw
            .text(status.icon_text)
            .font({
              size: fontSize,
              anchor: 'middle',
              leading: 1.4,
              fill: 'black'
            })
            .translate(centerPosition.x + 10, centerPosition.y - 35 - fontSize)
        }
      }
    }
  })
}

export default {
  getHex
}
