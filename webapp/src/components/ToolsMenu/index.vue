<template>
  <div :class="['connect-menu', {'aside-opened' : asideOpened}]">
    <card>
      <ul>
        <li @click="goTo('office')" :class="{'active' : $route.name === 'office'}">
          <font-awesome-icon icon="hotel" />
        </li>
        <li @click="goTo('reports')" :class="{'active' : $route.name === 'reports'}">
          <font-awesome-icon icon="chart-pie" />
        </li>
      </ul>
    </card>

    <card>
      <ul>
        <li @click="handleNotifications" :class="{'active': isNotificationsActive && asideOpened}">
          <font-awesome-icon icon="bell" />
        </li>
        <li @click="handleBoard" :class="{'active': isBoardActive && asideOpened}">
          <font-awesome-icon icon="chalkboard" />
        </li>
        <li @click="handleReleases" :class="{'active': isReleasesActive && asideOpened}">
          <font-awesome-icon icon="star" />
        </li>
      </ul>
    </card>
  </div>
</template>
<script>
import { mapState } from "vuex";
import Card from "@/components/Card.vue";
export default {
  name: "ToolsMenu",
  components: {
    Card
  },
  props: {
    asideOpened: {
      type: Boolean
    }
  },
  data() {
    return {};
  },
  computed: {
    ...mapState({
      isBoardActive: state => state.app.isBoardActive,
      isNotificationsActive: state => state.app.isNotificationsActive,
      isReleasesActive: state => state.app.isReleasesActive
    })
  },
  methods: {
    handleBoard() {
      if (this.isNotificationsActive)
        this.$store.commit("setNotificationsActive");
      if (this.isReleasesActive) this.$store.commit("setReleasesActive");
      if (!this.asideOpened || this.isBoardActive)
        this.$store.commit("setAsideLeftActive");
      this.$store.commit("setBoardActive");
      this.$store.dispatch('getList')
      this.$store.dispatch('getBirthdays')
    },
    handleNotifications() {
      if (this.isBoardActive) this.$store.commit("setBoardActive");
      if (this.isReleasesActive) this.$store.commit("setReleasesActive");
      if (!this.asideOpened || this.isNotificationsActive)
        this.$store.commit("setAsideLeftActive");
      this.$store.commit("setNotificationsActive");
    },
    handleReleases() {
      if (this.isBoardActive) this.$store.commit("setBoardActive");
      if (this.isNotificationsActive)
        this.$store.commit("setNotificationsActive");
      if (!this.asideOpened || this.isReleasesActive)
        this.$store.commit("setAsideLeftActive");
      this.$store.commit("setReleasesActive");
    },
    goTo(to) {
      this.$router.push({ name: to });
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-menu {
  position: fixed;
  top: 71px;
  left: $margin-left-container;
  width: 50px;
  transition: $aside-transition;

  &.aside-opened {
    left: $margin-left-container-aside-opened;
  }

  .connect-card {
    margin-bottom: 15px;
  }

  ul {
    padding: 10px 5px;
    margin: 0 auto;
    list-style: none;

    li {
      margin: 0 auto;
      width: 40px;
      height: 40px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      svg {
        z-index: 2;
      }

      &:hover {
        cursor: pointer;

        svg:not(.non-lineal) path {
          fill: $primary;
        }

        svg.non-lineal path {
          fill: none;
          stroke: $primary;
        }
      }

      &.active {
        &:before {
          content: "";
          position: absolute;
          z-index: 1;
          top: 0;
          left: 0;
          bottom: 0;
          right: 0;
          border-radius: 50%;
          background: $light-gray;
        }

        svg:not(.non-lineal) path {
          fill: $primary;
        }

        svg.non-lineal path {
          fill: none;
          stroke: $primary;
        }
      }
    }
  }
}
</style>