<template>
  <div class="connect-birthday-board" :style="`background-image: url(${birthdayLogo});`">
    <h4>Próximos cumpleañeros</h4>
    <ul>
      <li v-for="item in filteredList" :key="item.id">
        <Avatar :img="item.avatar_thumb" :text="when(item.birthday)" />
      </li>
      <li v-if="list.length > 4" class="connect-birthday-indicator">{{howManyMore}}</li>
    </ul>
  </div>
</template>
<script>
import Avatar from "@/components/Avatar";
import birthdayPng from "@/assets/birthday.png";
export default {
  name: "Birthdays",
  components: {
    Avatar
  },
  props: {
    list: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      birthdayLogo: birthdayPng
    };
  },
  computed: {
    filteredList() {
      return this.list.slice(0, 4);
    },
    howManyMore() {
      const length = this.list.length - 4;

      if (length > 99) return "+99";
      return length;
    }
  },
  methods: {
    when(brth) {
      const currentYear = new Date().getFullYear();
      const brthFormat = `${currentYear}${brth.substring(4)}`;
      return this.$moment(brthFormat).calendar(null, {
        sameDay: "[Hoy]",
        nextDay: "[Mañana]",
        nextWeek: "DD/MM",
        nextMonth: "DD/MM",
        sameElse: "L"
      });
    }
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
