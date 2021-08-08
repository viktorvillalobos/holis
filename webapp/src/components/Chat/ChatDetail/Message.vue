<template>
  <div class="chat-message">
    <div class="columns">
        <Avatar :img="message.avatar_thumb" style="margin-top:10px; margin-left:20px" />
        <div class="column">
            <p class="chat-message-date"><b class="chat-message-title">{{ message.who}}</b>   {{ message.getDateTime() }}</p>
            <p v-html="message.text"></p>
            <div
              v-if="message.text.length > 0 || message.text !== '<p></p>'">
                <Attachment v-if="message.attachments.length > 0" :attachment="message.attachments[0]"/>
            </div>

            <div
              v-for="attachment in message.attachments.slice(1)" :key="attachment.attachment_url">
              <Attachment class="image-message" :attachment="attachment"/>
            </div>
        </div>
    </div> 
    <div class="chat-message-divider"></div>
  </div>
</template>
<script>
import Avatar from '@/components/Avatar'
import { Message } from '../../../models/Message'
import Attachment from './Attachment'

export default {
  name: 'Message',
  props: {
    message: {
      type: Message
    }
  },
  components: { Avatar, Attachment }
}
</script>
<style lang="scss">
.chat-message{
  font-family: $family-dm-sans;
  padding-top: 20px;
  padding-bottom: 10px;

  &-title{
    color: #2D343C;
    font-size: 14px;
    padding-bottom: 10px;
  }

  &-date{
    color: #828282;
    font-size: 12px;
  }

  ul{
    list-style-type: circle;
    padding: 0 1.1rem;
  }
  ol {
    padding: 0 1rem;
  }

  blockquote {
    padding-left: 1rem;
    padding-top: 3px;
    padding-bottom: 3px;
    border-left: 2px solid $dark-blue;
  }

  pre, code {
    padding-top: 5px;
    padding-bottom: 5px;
    margin-top: 3px;
    margin-bottom: 3px;
    background: $dark-blue;
    color: #fff;
    border-radius:4px;
  }
  
}


.connect-chat-message {
  padding: 7px;
  background: $primary;
  color: #fff;
  border-radius: 8px 8px 8px 0;
  font-size: 13px;

  ul{
    list-style-type: circle;
    padding: 0 1.1rem;
  }
  ol {
    padding: 0 1rem;
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(white, 1);
  }

  /** {
    color: #fff;
  }*/

  pre, code {
    background: $dark-blue;
    color: #fff;
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
