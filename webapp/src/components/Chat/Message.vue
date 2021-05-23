<template>
  <div
    :class="['connect-chat-message-wrapper', {'connect-chat-message-wrapper--mine' : message.messageIsMine}]"
  >
    <div
      :class="['connect-chat-message', {'connect-chat-message--mine' : message.messageIsMine}]"
      v-html="message.text">
    </div>

{{message}}
    <div v-for="attachment in message.attachments" :key="attachment.attachment_url">
      {{ attachment.attachment_url }}
      <img :src="attachment.attachment_url">
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

export default {
  name: 'Message',
  props: {
    message : {
      type: Message
    }
  },
  components: { Avatar }
}
</script>
<style lang="scss">
.connect-chat-message {
  padding: 7px;
  background: $primary;
  color: #fff;
  border-radius: 8px 8px 8px 0;
  font-size: 13px;

  * {
    color: #fff;
  }

  pre, code {
    background: $dark-blue;
    border-radius:4px ;
  }

  &--mine {
    border-radius: 8px 8px 0 8px;
  }

  &-wrapper {
    min-width: 262px;
    max-width: 90%;
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
</style>
