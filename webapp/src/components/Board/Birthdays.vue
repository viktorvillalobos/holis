<template>
  <div class="connect-birthday-board">
    <h4>Próximos cumpleañeros</h4>
    <ul>
      <li>
        <Avatar text="Hoy" />
      </li>
      <li>
        <Avatar text="Mañana" />
      </li>
      <li>
        <Avatar text="Mañana" />
      </li>
      <li class="connect-birthday-indicator">+99</li>
    </ul>
  </div>
</template>
<script>
import Avatar from "@/components/Avatar";
export default {
  name: "Birthdays",
  components: {
    Avatar
  }
};
</script>
<style lang="scss" scoped>
.connect-birthday {
  &-board {
    border-radius: 4px;
    background: $primary;
    position: relative;
    color: #fff;
    padding: 4px 10px;
    background-image: url(../../assets/birthday.png);
    background-repeat: no-repeat;
    background-position: bottom right;

    h4 {
      margin: 0 0 4px 0;
    }

    ul {
      list-style: none;
      padding: 0;
      margin: 0;
      display: inline-flex;

      li {
        margin-right: 9px;

        &.connect-birthday-indicator {
          width: 42px;
          height: 42px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          background: $blue-dark;
          cursor: pointer;
        }
      }
    }
  }
}
</style>