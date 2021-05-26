<template>
  <div
    :class="['connect-chat-message-wrapper', {'connect-chat-message-wrapper--mine' : message.messageIsMine}]"
  >
    <div
      v-if="message.text.length > 0 || message.text !== '<p></p>'"
      :class="['connect-chat-message', {'connect-chat-message--mine' : message.messageIsMine}]">
        <Attachment v-if="message.attachments.length > 0" :attachment="message.attachments[0]"/>
        <p v-html="message.text"></p>
    </div>

    <div 
      :class="['connect-chat-message', 'attachment', {'connect-chat-message--mine' : message.messageIsMine}]"
      v-for="attachment in message.attachments.slice(1)" :key="attachment.attachment_url">
      <Attachment class="image-message" :attachment="attachment"/>
    </div>

    <div class="connect-chat-message-user">
      <Avatar v-if="!message.messageIsMine" :img="message.avatar"/>
      <p>{{ message.messageIsMine ? 'You' : message.who}} · {{ message.getDateTime() }}</p>
    </div>
  </div>
</template>
<script>
import Avatar from '@/components/Avatar'
import Message from '../../models/Message'
import Attachment from './Attachment'

export default {
  name: 'Message',
  props: {
    message : {
      type: Message
    }
  },
  components: { Avatar, Attachment }
}
</script>
<style lang="scss">
.connect-chat-message {
  padding: 7px;
  background: $primary;
  color: #fff;
  border-radius: 8px 8px 8px 0;
  font-size: 13px;

  /** {
    color: #fff;
  }*/

  pre, code {
    background: $dark-blue;
    border-radius:4px ;
  }

  &--mine {
    border-radius: 8px 8px 0 8px;
  }

  &-wrapper {
    min-width: 262px;
    max-width: 60%;
    margin-bottom: 10px;

    &--mine {
      align-self: flex-end;

      .connect-chat-message-user {
        p {
            margin: 0
        }
      }
    }
  }

  &-user {
    display: flex;
    align-items: flex-start;
    font-size: 12px;
    margin-top: 5px;

    .connect-avatar {
      width: 30px;
      height: 30px;
    }

    p {
      margin-left: 10px;
    }
  }
}

.attachment{
  margin-top: 10px;
}
</style>
