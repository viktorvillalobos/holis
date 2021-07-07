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
    <div>
      <editor-content :editor="editor" class="editor-content"  />
      <div class="columns" style="padding-bottom:10px">
        <div class="editor-buttons"></div>
        <div v-if="editor" class="column" style="z-index:1">
          <button @click="editor.chain().focus().toggleBold().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('bold') }">
            <font-awesome-icon icon="bold" />
          </button>
          <button @click="editor.chain().focus().toggleItalic().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('italic') }">
            <font-awesome-icon icon="italic" />
          </button>
          <button @click="editor.chain().focus().toggleStrike().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('strike') }">
            <font-awesome-icon icon="strikethrough" />
          </button>
          <button @click="editor.chain().focus().toggleCode().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('code') }">
            <font-awesome-icon icon="code" />
          </button>
          <button @click="editor.chain().focus().toggleBulletList().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('bulletList') }">
          <font-awesome-icon icon="list-ul" />
          </button>
          <button @click="editor.chain().focus().toggleOrderedList().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('orderedList') }">
            <font-awesome-icon icon="list-ol" />
          </button>
          <button @click="editor.chain().focus().toggleCodeBlock().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('codeBlock') }">
            <font-awesome-icon icon="code" />
          </button>
          <button @click="editor.chain().focus().toggleBlockquote().run()" class="menubar__button" :class="{ 'is-active': editor.isActive('blockquote') }">
            <font-awesome-icon icon="quote-left" />
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
        <div class="column" align="right" style="z-index:1">
            <button
              class="menubar__button menubar__button__send"
              @click="submit"
              :class="{ 'is-active': isSendActive }">
                <span class="material-icons" style="font-size:18px">send</span>
            </button>
        </div>
      </div>
  </div>
  <VEmojiPicker v-if="showEmojiPicker" @select="selectEmoji" />
  </div>
</template>
<script>
import VEmojiPicker from 'v-emoji-picker'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Editor, EditorContent } from '@tiptap/vue-2'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import BulletList from '@tiptap/extension-bullet-list'

export default {
  components: {
    EditorContent,
    VEmojiPicker,
    FontAwesomeIcon
  },
  props: {
    modelValue: {
      type: String,
      default: '',
    },
  },
  data () {
    return {
      showEmojiPicker: false,
      message: '',
      editor: null,
      isSendActive: false,
      files: []
    }
  },
  mounted () {
    const vm = this
    window.$chatEditor = this
    this.editor = new Editor({
      content: this.modelValue,
      extensions: [
        StarterKit,
        Placeholder,
        BulletList.extend({
          addKeyboardShortcuts() {
            return {
              // ↓ your new keyboard shortcut
              'Enter': () => vm.submit(),
            }
          }})
      ],
      onUpdate: () => {
        this.isSendActive = this.editor.getHTML()
                                        .replaceAll("<p>","")
                                        .replaceAll("</p>","")
                                        .replaceAll("<br>","") !== ""
      },})
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
      const end = this.editor.getHTML().lastIndexOf('</p>')
      const content = `${this.editor.getHTML().slice(0, end)}${emoji.data}</p>`

      this.editor.commands.setContent(content, true)
      this.showEmojiPicker = false
    },
    clearEditor() {
      this.editor.commands.setContent("", true)
      this.editor.commands.clearContent(true)
      this.editor.commands.clearNodes()
      this.$refs.chatFileInput.value = null
      this.files = []
      this.showEmojiPicker = false
      this.isSendActive = false
      console.log("TUNDIIPUTAMDREE",this.editor
                .getHTML())
    },
    submit () {
      if(!this.isSendActive)
        return

      const messageText =
                this.editor
                .getHTML()
                .replaceAll("<p></p>","</br>")

      const messageObj = {
        message: messageText,
        is_mine: true,
        datetime: new Date(),
        files: this.files
      }

      this.clearEditor()
      this.$emit('sendMessage', messageObj)
    }
  }
}
</script>

<style lang="scss">
.editor-buttons{
  //margin: 0px -10px 0px -10px;
  margin-top: 2px;
  margin-left: 12px;
  position: absolute;
  z-index: 0;
  height: 50px;
  width: 100%;
  background: #F2F2F2;
  border-radius: 0px 0px 2px 2px;
}
.editor-content{
  padding: 20px 10px 20px 10px;
}
.ProseMirror {
  > * + * {
    //margin-top: 0.75em;
  }

  &:focus{
    outline: none;
  }

  ul{
    list-style-type: circle;
    padding: 0 1.2rem;
  }
  ol {
    padding: 0 1rem;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
  }

  code {
    background-color: rgba(#616161, 0.1);
    color: #616161;
  }

  pre {
    background: $dark-blue;
    color: #FFF;
    font-family: 'JetBrainsMono', monospace;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;

    code {
      color: inherit;
      padding: 0;
      background: none;
      font-size: 0.8rem;
    }
  }

  img {
    max-width: 100%;
    height: auto;
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(#0D0D0D, 0.1);
  }

  hr {
    border: none;
    border-top: 2px solid rgba(#0D0D0D, 0.1);
    margin: 2rem 0;
  }
}

.ProseMirror p.is-editor-empty:first-child::before {
    content: attr(data-placeholder);
    float: left;
    color: #ced4da;
    pointer-events: none;
    height: 0;
}

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
  border: 1px solid #F2F2F2;
  margin: 20px 13px 18px 9px;
  

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
      height: 30px;
      width: 30px;
      padding: 4px 8px;
      margin-left: 5px;
      border-radius: 15px;

      &:hover {
        cursor: pointer;
        background: $lighter-gray;
      }

      &.is-active {
          background-color: $primary;
          color: #fff;
      }

      &__send {
        margin-right: 10px; 
        color: #BDBDBD;

        &.is-active {
          background-color: $primary;
          color: #fff;
        }
      }
    }
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
