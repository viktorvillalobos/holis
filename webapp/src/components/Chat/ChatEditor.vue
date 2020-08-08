<template>
  <div class="holis-chat-editor">
    <editor-menu-bar :editor="editor">
      <div class="menubar" slot-scope="{ commands, isActive }">
        <div>
          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.bold() }"
            @click="commands.bold"
          >
            <font-awesome-icon icon="bold" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.italic() }"
            @click="commands.italic"
          >
            <font-awesome-icon icon="italic" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.strike() }"
            @click="commands.strike"
          >
            <font-awesome-icon icon="strikethrough" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.underline() }"
            @click="commands.underline"
          >
            <font-awesome-icon icon="underline" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.code() }"
            @click="commands.code"
          >
            <font-awesome-icon icon="code" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.bullet_list() }"
            @click="commands.bullet_list"
          >
            <font-awesome-icon icon="list-ul" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.ordered_list() }"
            @click="commands.ordered_list"
          >
            <font-awesome-icon icon="list-ol" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.blockquote() }"
            @click="commands.blockquote"
          >
            <font-awesome-icon icon="quote-left" />
          </button>

          <button
            class="menubar__button"
            :class="{ 'is-active': isActive.code_block() }"
            @click="commands.code_block"
          >
            <font-awesome-icon icon="code" />
          </button>
          <button class="menubar__button" click>
            <font-awesome-icon icon="paperclip" />
          </button>
          <button class="menubar__button" @click="showEmojiPicker = !showEmojiPicker">
            <font-awesome-icon icon="grin-squint-tears" />
          </button>
        </div>

        <div>
          <button
            class="menubar__button menubar__button__send"
            @click="submit"
            :class="{ 'is-active': isSendActive }"
          >
            <font-awesome-icon icon="paper-plane" />
          </button>
        </div>
      </div>
    </editor-menu-bar>
    <editor-content class="editor__content" :editor="editor" />
    <VEmojiPicker v-if="showEmojiPicker" @select="selectEmoji" />
  </div>
</template>
<script>
import VEmojiPicker from "v-emoji-picker";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { Editor, EditorContent, EditorMenuBar } from "tiptap";
import {
  Blockquote,
  CodeBlock,
  HardBreak,
  Heading,
  HorizontalRule,
  OrderedList,
  BulletList,
  ListItem,
  TodoItem,
  TodoList,
  Bold,
  Code,
  Italic,
  Link,
  Strike,
  Underline,
  History,
} from "tiptap-extensions";

export default {
  components: {
    VEmojiPicker,
    EditorContent,
    EditorMenuBar,
    FontAwesomeIcon,
  },
  data() {
    return {
      showEmojiPicker: false,
      message: "",
      editor: new Editor({
        extensions: [
          new Blockquote(),
          new BulletList(),
          new CodeBlock(),
          new HardBreak(),
          new Heading({ levels: [1, 2, 3] }),
          new HorizontalRule(),
          new ListItem(),
          new OrderedList(),
          new TodoItem(),
          new TodoList(),
          new Link(),
          new Bold(),
          new Code(),
          new Italic(),
          new Strike(),
          new Underline(),
          new History(),
        ],
        content: "",
      }),
      isSendActive: false,
    };
  },
  mounted() {
    let self = this;
    this.editor.on("update", ({ state, getHTML, getJSON }) => {
      const newContent = getHTML();
      console.log("ugh", getHTML(), getJSON());
      if (newContent !== "<p></p>") {
        this.isSendActive = true;
      } else {
        this.isSendActive = false;
      }

      this.message = newContent;
    });
  },
  beforeDestroy() {
    this.editor.destroy();
  },
  methods: {
    selectEmoji(emoji) {
      this.message = this.message + emoji.data;
      this.showEmojiPicker = false;
    },
    submit() {
      const msg = {
        message: this.message,
        is_mine: true,
        datetime: new Date(),
      };
      this.$emit("enter", msg);

      this.editor.clearContent()
    },
  },
};
</script>
<style lang="scss" scoped>
.field:not(:last-child) {
  margin-bottom: 0;
}

.holis-chat-editor {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  border-radius: 4px;
  background: #fff;
  border: 1px solid $medium-gray;
  margin: 20px 13px 18px 9px;
  .field {
    background: $light-gray;
    border: 0;
    border-radius: 4px;
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

  .menubar {
    background: $light-gray;
    height: 34px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    &__button {
      border: 0;
      background: transparent;
      color: $gray;
      padding: 4px 8px;
      margin-left: 5px;
      border-radius: 4px;

      &:hover {
        cursor: pointer;
        background: $lighter-gray;
      }

      &__send {
        margin-right: 15px;

        &.is-active {
          background-color: $primary;
          color: #fff;
        }
      }
    }
  }

  .editor__content {
    padding: 4px 12px;
  }
}

#EmojiPicker {
  width: 300px;
  position: absolute;
  bottom: 100%;

  .emoji {
    padding-top: 7px;
  }
}
</style>
