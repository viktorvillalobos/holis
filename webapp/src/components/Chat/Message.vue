<template>
  <div
    :class="['connect-chat-message-wrapper', {'connect-chat-message-wrapper--mine' : messageIsMine}]"
  >
    <div
      :class="['connect-chat-message', {'connect-chat-message--mine' : messageIsMine}]"
      v-html="msg.message"
    ></div>
    <div class="connect-chat-message-user">
      <Avatar v-if="!messageIsMine" />
      <p>{{ messageIsMine ? 'You' : who}} · {{ datetime | moment("ddd, hA")}}</p>
    </div>
  </div>
</template>
<script>
import Avatar from '@/components/Avatar'
export default {
  name: 'Message',
  props: {
    messageIsMine: {
      type: Boolean
    },
    msg: {
      type: Object
    },
    datetime: {
      type: Date
    },
    who: {
      type: String
    },
    id: {
      type: String
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
