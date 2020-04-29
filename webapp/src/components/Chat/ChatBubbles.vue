<template>
  <ul class="connect-chat-bubbles">
    <li>
      <Btn>chevron</Btn>
    </li>
    <li>
      <Btn>Plus</Btn>
    </li>
    <li>
      <Avatar />
    </li>
  </ul>
</template>
<script>
import Avatar from "@/components/Avatar";
import Btn from "@/components/Btn";
export default {
  name: "ChatBubbles",
  components: {
    Avatar,
    Btn
  }
};
</script>
<style lang="scss" scoped>
.connect-chat-bubbles {
  list-style: none;
  padding: 0;
  text-align: center;

  li {
    margin: 7px;
  }
}
</style>