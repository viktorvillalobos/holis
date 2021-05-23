<template>
  <div>
    <img v-if="attachment.isImage()" class="image-message" :src="attachment.attachment_url">
    <div v-else class="card card-attachment">
        <div class="columns">
            <div class="column is-one-fifth">
                <font-awesome-icon icon="file-alt" size="3x" style="color:grey"/>
            </div>
            <div class="column">
                <p class="is-4">{{ attachment.attachment_name }}</p>
                <p class="is-6">Descargar</p>
            </div>
        </div>
    </div>
  </div>
</template>
<script>
import { Attachment } from '../../models/Message'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

export default {
  name: 'Attachment',
  props: {
    attachment : {
      type: Attachment
    }
  },
  components: { FontAwesomeIcon }
}
</script>
<style lang="scss">
.image-message{
  width: 100%;
}
.card-attachment{
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 15px;
}
</style>
