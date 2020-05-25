<template>
  <div :class="['connect-logo-wrapper', {'aside-opened' : asideOpened}]">
    <img class="connect-logo-company" src="/static/images/logo/Espazum.png" alt="espazum logo" width="200"/>
    <span class="connect-separator">|</span>
    <h1 class="connect-company">{{ company.name }}</h1>
  </div>
</template>

<script>
/**
 * The wrapper of the logos :D
 * @displayName Logo
 */
export default {
  name: "Logo",
  props: {
    /**
     * The data of the company name and logo, if logo is not provided it will be replaced by the company name as text
     */
    company: {
      type: Object,
      default: () => {
        return {
          name: "Tacata Inc.",
          logo: null
        };
      }
    },
    asideOpened: {
      type: Boolean
    }
  },
  computed: {
    name () {
      return `| ${this.company.name}`
    }
  }
};
</script>

<style lang="scss" scoped>
.connect-logo {
  max-height: 46px;
  &-wrapper {
    display: flex;
    position: fixed;
    top: 0;
    left: $margin-left-container;
    align-items: center;
    justify-content: center;
    padding: 7px 9px 7px 0;
    transition: $aside-transition;

    &.aside-opened {
      left: $margin-left-container-aside-opened;
    }

    .connect-company {
      font-weight: bold;
      font-size: 22px;
      margin-top: 2.6%;
      padding-left: 3%;
    }

    .connect-separator {
      color: #576fe9;
      font-weight: bold;
      font-size: 26px;
      padding: 0 0 0 15px;
      margin-top: 2%;
    }
  }

}


.connect-logo-company {
  margin-top: 5%;
  margin-left: 2%;
}

</style>
