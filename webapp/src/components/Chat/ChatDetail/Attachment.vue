<template>
  <div>
    <img v-if="attachment.isImage()" @click="openImage(attachment.attachment_url)" class="image-message" :src="attachment.attachment_url">
    <div v-else class="card card-attachment" @click="downloadFile(attachment.attachment_url)">
        <div class="columns">
            <div class="column is-one-fifth">
                <font-awesome-icon icon="file-alt" size="3x" style="color:$primary"/>
            </div>
            <div class="column" >
                <p class="is-size-6 has-text-black">{{ attachment.attachment_name }}</p>
                <p class="is-size-7 has-text-primary">Descargar</p>
            </div>
        </div>
    </div>

    <div :class="{'modal' : true, 'is-active' : url != ''}" style="z-index:100"> <!-- Coloque 100 por que el chat header tiene 99 ni idea por q-->
      <div class="modal-background"></div>
      <div class="modal-content">
        <img :src="url" class="zoom"/>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="url=''"></button>
    </div>

  </div>
</template>
<script>
import { Attachment } from '../../../models/Message'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

export default {
  name: 'Attachment',
  props: {
    attachment: {
      type: Attachment
    }
  },
  data () {
    return {
      url: ''
    }
  },
  components: { FontAwesomeIcon },
  methods: {
    openImage (url) {
      this.url = url
    },
    downloadFile (url) {
      const link = document.createElement('a')
      link.href = url
      link.download = url.substr(url.lastIndexOf('/') + 1)
      link.click()
    }
  }
}
</script>
<style lang="scss">
.image-message{
  width: 100%;
  cursor: pointer !important;
}
.card-attachment{
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 15px;
  cursor: pointer !important;
}

.zoom:hover {
  transform: scale(1.5); /* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
}
</style>
