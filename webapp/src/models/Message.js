import moment from 'moment'

export default class Message{

  constructor(map) {
      console.log(map)
      this.id = map.uuid
      this.messageIsMine = this.getIsMine(map.user_id)
      this.who = map.user_name
      this.created = map.created
      this.text = map.text
      this.avatar = map.avatar
      this.avatar_thumb = map.avatar_thumb
      this.showDate = map.showDate
      if(map.attachments !== undefined){
          const attachments = map.attachments
          this.attachments = attachments.map(attachment => new Attachment(attachment))
      }else{
          this.attachments = []
      }
  }

  getIsMine (userId) {
    return userId === window.user_id
  }

  getDateTime () {
    const date = moment(this.created).format('ddd, h:mm a').replace('.', '')
    return date.charAt(0).toUpperCase() + date.slice(1)
  }
}

export class Attachment {
  constructor (map) {
    this.attachment_mimetype = map.attachment_mimetype
    this.attachment_url = map.attachment_url
    if (map.attachment_name !== undefined) { this.attachment_name = map.attachment_name } else { this.attachment_name = 'Texto de prueba' }
  }

  isImage(){
      return (this.attachment_mimetype.includes('image/png') ||
              this.attachment_mimetype.includes('image/jpg') ||
              this.attachment_mimetype.includes('image/jpeg'))
  }
}
