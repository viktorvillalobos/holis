<template>
  <div>
    <div
      @click="$emit('btn-click')"
      :class="[
    'connect-btn', 
    {'connect-btn--outline' : outline}, 
    {'connect-btn--dropdown' : dropdown},
    {'connect-btn--flat' : flat},
    {'connect-btn--primary' : primary},
    {'connect-btn--inverse' : inverse},
    {'connect-btn--round' : round},
    {'connect-btn--icon' : icon}
    ]"
      :style="size ? `width: ${size}px; height: ${size}px` : ''"
    >
      <span>
        <slot />
      </span>
      <div
        v-if="dropdown"
        @click.stop="dropdownActive = !dropdownActive"
        class="connect-btn-drop-action"
      >
        <img src="@/assets/icons/chevron-down.svg" />
      </div>
    </div>
    <card class="outside-card" v-if="dropdown && dropdownActive">
      <slot name="options" />
    </card>
  </div>
</template>
<script>
/**
 * The best button in the world
 * @displayName Button
 */
import Card from "@/components/Card";
export default {
  props: {
    /**
     * Determines wether or not the button is flat
     */
    flat: {
      type: Boolean,
      default: false
    },
    /**
     * Determines wether or not the button is flat
     */
    size: {
      type: Number
    },
    /**
     * Determines wether or not the button is flat
     */
    round: {
      type: Boolean,
      default: false
    },
    /**
     * Determines wether or not the button is flat
     */
    icon: {
      type: Boolean,
      default: false
    },
    /**
     * Determines wether or not the button is outline
     */
    outline: {
      type: Boolean,
      default: false
    },
    /**
     * Determines if the button is droppable
     */
    dropdown: {
      type: Boolean,
      default: false
    },
    /**
     * Determines if the button is color primary
     */
    primary: {
      type: Boolean,
      default: false
    },
    /**
     * Determines if the button is inverse
     */
    inverse: {
      type: Boolean,
      default: false
    }
  },
  components: {
    Card
  },
  data() {
    return {
      dropdownActive: false
    };
  }
};
</script>
<style lang="scss">
.connect-btn {
  padding: 7px 14px;
  border-radius: 4px;
  position: relative;
  cursor: pointer;

  span {
    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Old versions of Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Opera and Firefox */
  }

  &--outline {
    border: 1px solid;
  }

  &--primary {
    background: $primary;
    color: #fff;

    &:hover {
      box-shadow: 0 0 0 4px rgba(47, 128, 237, 0.2);
    }
  }

  &--inverse {
    background: #fff;
    color: $primary;

    &:hover {
      box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.2);
    }
  }

  &--flat {
    background: transparent;
    color: $primary;

    &:hover {
      box-shadow: none;
      background: rgba(47, 128, 237, 0.2);
    }
  }

  &--round {
    border-radius: 50%;
  }

  &--icon {
    padding: 0;
    > span {
      width: 100%;
      height: 100%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
  }

  &--dropdown {
    padding-right: 33px;
    .connect-btn-drop-action {
      position: absolute;
      right: 0;
      top: 0;
      bottom: 0;
      width: 29px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.1);
    }
  }
}

.outside-card {
  position: absolute;
  ul {
    li {
      padding: 5px 15px;
    }
  }
}
</style>