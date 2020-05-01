<template>
  <div class="connect-chat-header">
    <h3>{{chatName}}</h3>
    <ul class="chat-actions">
      <li>
        <font-awesome-icon icon="search" />
      </li>
      <li>
        <font-awesome-icon icon="plus" />
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  props: {
    chatName: {
      type: String,
      default: "Chat name"
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 2px 15px;

  .chat-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;

    li {
        margin-left: 5px;
        cursor: pointer;
    }
  }
}

#EmojiPicker {
    width: 300px;
    position: absolute;
    bottom: 100%;

    .emoji {
        padding-top: 7px;
    }
}
</style>