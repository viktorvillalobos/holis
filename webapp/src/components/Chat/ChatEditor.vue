<template>
  <div class="holis-chat-editor">
    <div v-show="files.length" class="files-slot">
      <ul>
        <li v-for="(file, index) in files" :key="index">
          <div class="file-icon">
            <img v-if="file.type.includes('image')" :src="fileBlob(file)" :alt="file.name" />
            <font-awesome-icon
              v-if="file.type.includes('video') && !file.type.includes('image')"
              icon="video"
            />
            <font-awesome-icon
              v-else-if="!file.type.includes('video') && !file.type.includes('image')"
              icon="file-alt"
            />
          </div>
          <div class="file-info">{{file.name}}</div>
          <button @click="removeFile(index)" class="button is-white">
            <span class="icon is-small">
              <font-awesome-icon icon="times" />
            </span>
          </button>
        </li>
      </ul>
    </div>
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
          <button class="menubar__button" @click="handleFileInput">
            <input
              type="file"
              multiple
              ref="chatFileInput"
              @change="filesSelected"
              class="holis-chat-editor-file-input"
            />
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
            <font-awesome-icon icon="paper-plane"  />
          </button>
        </div>
      </div>
    </editor-menu-bar>
    <editor-content class="editor__content" :editor="editor"/>
    <VEmojiPicker v-if="showEmojiPicker" @select="selectEmoji" />
  </div>
</template>
<script>
import VEmojiPicker from 'v-emoji-picker'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Editor, EditorContent, EditorMenuBar } from 'tiptap'
import { EnterHandler } from './Extensions'

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
  History
} from 'tiptap-extensions'

export default {
  components: {
    VEmojiPicker,
    EditorContent,
    EditorMenuBar,
    FontAwesomeIcon
  },
  data () {
    return {
      showEmojiPicker: false,
      message: '',
      editor: new Editor({
        extensions: [
          new EnterHandler(),
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
          new History()
        ],
        content: ''
      }),
      isSendActive: false,
      files: []
    }
  },
  mounted () {
    window.$chatEditor = this
    this.editor.on('update', ({ state, getHTML, getJSON }) => {
      const newContent = getHTML()
      if (newContent !== '<p></p>') {
        this.isSendActive = true
      } else {
        this.isSendActive = false
      }

      this.message = newContent
    })
  },
  beforeDestroy () {
    this.editor.destroy()
  },
  methods: {
    handleFileInput () {
      this.$refs.chatFileInput.click()
    },
    filesSelected (e) {
      this.files = []
      e.target.files.forEach((x) => {
        console.log('file', x)
        this.files.push(x)
      })
    },
    fileBlob (e) {
      return URL.createObjectURL(e)
    },
    removeFile (index) {
      this.files.splice(index, 1)
    },
    selectEmoji (emoji) {
      const end = this.message.lastIndexOf('</p>')
      const content = `${this.message.slice(0, end)}${emoji.data}</p>`

      this.editor.setContent(content, true)
      this.showEmojiPicker = false
    },
    submit () {
      console.log("ENTERRRRR")
      const msg = {
        message: this.message,
        is_mine: true,
        datetime: new Date(),
        files: this.files
      }
      console.log(msg)
      this.$emit('enter', msg)
      this.editor.clearContent()
      this.showEmojiPicker = false
      this.message = '<p></p>'
    }
  }
}
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

  &-file-input {
    display: none;
  }

  .files-slot {
    position: absolute;
    bottom: calc(100% + 7px);
    width: 100%;

    ul {
      display: flex;
      background: #fff;
      border-radius: 4px;
      border: 1px solid $medium-gray;
      padding: 10px 8px;
      max-width: 100%;
      overflow-x: auto;
      li {
        display: flex;
        width: 230px;
        height: 66px;
        background: $light-gray;
        border-radius: 4px;
        padding: 10px 8px;
        justify-content: space-between;
        margin-right: 8px;

        .file {
          &-icon {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            overflow: hidden;
            background-color: $medium-gray;
          }

          &-info {
            width: 120px;
            overflow: hidden;
            text-overflow: ellipsis;
          }
        }
      }
    }
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
