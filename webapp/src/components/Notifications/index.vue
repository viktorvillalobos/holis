<template>
  <div class="connect-notification-list">
    <Notification>
      <p>Tu reunion <strong>Daily</strong> está a punto de iniciar</p>
    </Notification>
    <Notification>
      <p>Tu reunion <strong>Daily</strong> está a punto de iniciar</p>
    </Notification>
    <Notification>
      <p>Tu reunion <strong>Daily</strong> está a punto de iniciar</p>
    </Notification>
  </div>
</template>
<script>
import Notification from "./Notification";
export default {
  name: "NotificationsList",
  components: {
    Notification
  }
};
</script>
<style lang="scss" scoped>
.connect-notification-list {
  padding: 15px;
}
</style>