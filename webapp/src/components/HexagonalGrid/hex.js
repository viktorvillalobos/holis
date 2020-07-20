import { extendHex } from 'honeycomb-grid'

function getHex (vmDraw, size) {
  return extendHex({
    size: size,
    user: null,
    image: null,
    status: null,
    voiceAnimation: [],
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
    createCircleAnimation (size, width) {
      const position = this.toPoint()
      const centerPosition = this.center().add(position)
      const reduce = size / 2
      return vmDraw.circle(size)
        .fill('#00000000')
        .translate(centerPosition.x - reduce, centerPosition.y - reduce)
        .stroke({ width, color: '#7f7fff' })
    },
    animateVoice (user) {
      const circle0 = this.createCircleAnimation(46, 1)
      const circle1 = this.createCircleAnimation(50, 1)
      const circle2 = this.createCircleAnimation(55, 1)

      circle1
        .animate({
          duration: 700,
          delay: 0,
          when: 'now',
          swing: true
        })
        .loop(true, true)
        .stroke({ width: 3, color: '#7f7fff' })

      circle2
        .animate({
          duration: 700,
          delay: 700,
          when: 'now',
          swing: true
        })
        .loop(true, true)
        .stroke({ width: 3, color: '#7f7fff' })

      this.voiceAnimation.push(circle0, circle1, circle2)
    },
    clearVoiceAnimation () {
      this.voiceAnimation.forEach(x => {
        x.node.remove()
      })
      this.voiceAnimation = []
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
      const size = 44
      const reduce = size / 2

      const img = vmDraw
        .image(avatar, size, size)
      fill = fill || img

      this.image = vmDraw.circle(size)
        .attr({ fill })
        .translate(centerPosition.x - reduce, centerPosition.y - reduce)
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
    addStatus (status) {
      status = status || this.user.status
      const position = this.toPoint()
      const centerPosition = this.center().add(position)
      const fontSize = 16
      if (this.user && this.user.status) {
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
  })
}

export default {
  getHex
}
