<template>
  <div class="connect-chat-editor">
    <div class="field">
      <p class="control has-icons-left has-icons-right">
        <input
          v-model="message"
          class="input is-small"
          type="text"
          placeholder="Escribe tu mensaje..."
        />
        <span class="icon-wrapper-files">
          <svg
            width="25"
            height="25"
            viewBox="0 0 25 25"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M16.6667 6.25V17.7083C16.6667 20.0002 14.7919 21.875 12.5 21.875C10.2082 21.875 8.33336 20.0002 8.33336 17.7083V5.7292C8.33336 4.27095 9.47926 3.125 10.9375 3.125C12.3957 3.125 13.5417 4.27095 13.5417 5.7292V17.7083C13.5417 18.2811 13.0727 18.75 12.5 18.75C11.9273 18.75 11.4583 18.2811 11.4583 17.7083V7.8125H9.89581V17.7083C9.89586 19.1666 11.0418 20.3125 12.5 20.3125C13.9583 20.3125 15.1042 19.1666 15.1042 17.7083V5.7292C15.1042 3.43755 13.2294 1.5625 10.9375 1.5625C8.64562 1.5625 6.77081 3.43755 6.77081 5.7292V17.7083C6.77086 20.8852 9.32316 23.4375 12.5 23.4375C15.6769 23.4375 18.2292 20.8852 18.2292 17.7083V6.25H16.6667Z"
              fill="#4F4F4F"
            />
          </svg>
        </span>
        <span class="icon-wrapper-emoji" @click="showEmojiPicker = !showEmojiPicker">
          <svg
            width="25"
            height="25"
            viewBox="0 0 25 25"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M12.5 1.5625C6.45937 1.5625 1.5625 6.45937 1.5625 12.5C1.5625 18.5406 6.45937 23.4375 12.5 23.4375C18.5406 23.4375 23.4375 18.5406 23.4375 12.5C23.4375 6.45937 18.5406 1.5625 12.5 1.5625ZM5.04258 12.3693C4.63867 12.0972 4.59097 11.6298 4.85962 11.285C5.37471 10.6237 6.01807 10.1562 7.03794 10.1562C8.05781 10.1562 8.70659 10.6247 9.21836 11.2878C9.48516 11.6333 9.4022 12.1184 9.03345 12.369C8.89111 12.4655 8.72383 12.5 8.54897 12.5C8.28472 12.5 8.03438 12.3966 7.87925 12.1962C7.71333 11.9806 7.50713 11.7188 7.03794 11.7188C6.57109 11.7188 6.36323 11.9818 6.19473 12.1983C6.04028 12.397 5.79072 12.5 5.52729 12.5C5.35244 12.5 5.18486 12.4652 5.04258 12.3693ZM19.2502 15.1829C18.096 17.4179 15.4465 18.75 12.5002 18.75C9.47925 18.75 6.76045 17.3713 5.73477 15.1525C5.55591 14.7648 5.72544 14.3037 6.1124 14.1243C6.2143 14.0772 6.32523 14.0528 6.4375 14.0529C6.73843 14.0529 7.01455 14.2292 7.14097 14.5021C7.91816 16.1835 10.0718 17.1875 12.5002 17.1875C14.8733 17.1875 16.9826 16.1978 17.8739 14.4719C17.939 14.3454 18.0377 14.2393 18.1592 14.1653C18.2807 14.0913 18.4203 14.0523 18.5625 14.0526C18.6862 14.0526 18.8096 14.0829 18.9194 14.1403C19.2969 14.3358 19.446 14.8039 19.2502 15.1829ZM19.971 12.369C19.8287 12.4654 19.6614 12.5 19.4865 12.5C19.2223 12.5 18.9719 12.3965 18.8167 12.1961C18.6508 11.9805 18.4447 11.7188 17.9754 11.7188C17.5086 11.7188 17.3008 11.9818 17.1323 12.1983C16.9778 12.397 16.7282 12.5 16.4648 12.5C16.2899 12.5 16.1223 12.4652 15.98 12.3693C15.5762 12.0972 15.5285 11.6298 15.7971 11.285C16.3122 10.6237 16.9556 10.1562 17.9754 10.1562C18.9954 10.1562 19.6441 10.6247 20.1559 11.2878C20.4227 11.6333 20.3397 12.1184 19.971 12.369Z"
              fill="#4F4F4F"
            />
          </svg>
        </span>
      </p>
    </div>
    <VEmojiPicker v-if="showEmojiPicker" @select="selectEmoji" />
  </div>
</template>
<script>
import VEmojiPicker from "v-emoji-picker";
export default {
  components: {
    VEmojiPicker
  },
  data() {
    return {
      showEmojiPicker: false,
      message: ""
    };
  },
  methods: {
    selectEmoji(emoji) {
      this.message = this.message + emoji.data;
      this.showEmojiPicker = false;
    }
  }
};
</script>
<style lang="scss" scoped>
.field:not(:last-child) {
  margin-bottom: 0;
}

.connect-chat-editor {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 3px 15px;

  &:before {
    content: "Presiona enter para enviar tu mensaje ;)";
    font-size: 10px;
  }

  input {
    background: $light-gray;
    border: 0;
  }

  [class*="icon-wrapper"] {
    position: absolute;
    top: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    width: 30px;

    &:hover {
      svg path {
        fill: $primary;
      }
    }
  }

  .icon-wrapper-files {
    left: 0;
    background: $medium-gray;
    border-radius: 4px 0 0 4px;
  }

  .icon-wrapper-emoji {
    right: 0;
  }
}
</style>