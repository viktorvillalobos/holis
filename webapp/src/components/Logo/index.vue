<template>
  <div :class="['connect-logo-wrapper', {'aside-opened' : asideOpened}]">
    <img class="connect-logo-company" src="/static/images/logo/logo.svg" alt="espazum logo" width="120"/>
    <div class="connect-separator"></div>
    <h1 class="connect-company">{{ company.name }}</h1>
  </div>
</template>

<script>
/**
 * The wrapper of the logos :D
 * @displayName Logo
 */
export default {
  name: 'Logo',
  props: {
    /**
     * The data of the company name and logo, if logo is not provided it will be replaced by the company name as text
     */
    company: {
      type: Object,
      default: () => {
        return {
          name: 'Tacata Inc.',
          logo: null
        }
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
}
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
      margin-top: 6.6%;
      padding-left: 3%;
    }

    .connect-separator {
      border-left: 1.5px solid #E9E9E9;
      height: 50px;
      margin-left: 15px;
      margin-right: 10px;
      margin-top: 10px;
    }
  }

}

.connect-logo-company {
  margin-top: 4%;
  margin-left: 2%;
}

</style>
