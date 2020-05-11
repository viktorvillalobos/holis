<template>
  <div :class="['connect-grid-user-card', origin]">
    <img src="@/assets/gridUserCardWaves.svg" class="connect-grid-user-card-waves" />
    <div class="connect-grid-user-card-content">
      <Avatar big />
      <div class="connect-grid-user-card-content-info">
        <h3>Joanna Davis</h3>
        <p class="position">Diseñadora</p>
        <p class="status">
          <font-awesome-icon icon="handshake" />En reunión
        </p>
      </div>
    </div>
    <ul class="connect-grid-user-card-actions">
      <li>
        <Btn primary>Chatea con ella</Btn>
      </li>
    </ul>
  </div>
</template>
<script>
import Avatar from "@/components/Avatar";
import Btn from "@/components/Btn";
export default {
  name: "GridUserCard",
  props: {
    origin: {
      type: String,
      default: "top"
    }
  },
  components: {
    Avatar,
    Btn
  }
};
</script>
<style lang="scss" scoped>
.connect-grid-user-card {
  width: 300px;
  height: 150px;
  border-radius: 8px;
  background: #fff;
  position: absolute;

  &:before {
    content: "";
    display: block;
    width: 16px;
    height: 16px;
    position: absolute;
    transform: rotate(45deg);
  }

  &.top {
    &:before {
      top: -8px;
      left: calc(50% - 8px);
      background-color: $primary;
    }
  }

  &.left {
    &:before {
      left: -8px;
      top: calc(50% - 8px);
      background-color: #9b51e0;
    }
  }

  &.right {
    &:before {
      right: -8px;
      top: calc(50% - 8px);
      background-color: #fff;
    }
  }

  &.bottom {
    &:before {
      bottom: -8px;
      left: calc(50% - 8px);
      background-color: #fff;
    }
  }

  &-waves {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1;
    border-radius: 8px 8px 0 0;
  }

  &-content {
    position: relative;
    z-index: 3;
    width: 100%;
    padding: 10px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 10px;

    &-info {
      color: #fff;
      width: 190px;

      h3 {
        font-size: 16px;
      }

      .position {
        font-size: 14px;
        margin-bottom: 9px;
      }

      .status {
        font-size: 12px;
        color: #000;
      }
    }
  }

  &-actions {
    padding: 0 10px 10px 10px;
    width: 100%;
    display: inline-flex;
    align-items: center;
    justify-content: flex-end;
  }
}
</style>