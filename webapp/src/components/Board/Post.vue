<template>
  <div class="connect-board-post">
    <div class="connect-board-post-title">
      <h3>{{post.title}}</h3>
      <ul>
        <li
          @click="handlePinPost"
          :class="['connect-board-post-pin', {'connect-board-post-pin--pinned' : isPinned}]"
        ></li>
      </ul>
    </div>
    <div class="connect-board-post-info">
      <Avatar :img="author.avatar_thumb" />
      <div class="connect-board-post-info-author">
        <p v-if="typeof author === 'object'">{{author.name}} · {{author.position}}</p>
        <p v-else>{{author}}</p>
        <p>{{post.created | moment('DD MMMM  [de] YYYY')}}</p>
      </div>
    </div>
    <div class="connect-post-content">
      <div>
        {{postContentToShow}}
        <a v-if="post.text.length > 140" class="expand-post" @click="expanded = !expanded">
          {{expanded ? 'Contraer' : 'Expandir'}}
          <img
            v-if="expanded"
            src="../../assets/icons/chevron-up.svg"
          />
          <img v-else src="../../assets/icons/chevron-down.svg" />
        </a>
      </div>
    </div>
  </div>
</template>
<script>
import Avatar from '@/components/Avatar'
export default {
  name: 'Post',
  props: {
    isPinned: {
      type: Boolean,
      default: false
    },
    post: {
      type: Object
    },
    author: {
      type: Object
    }
  },
  components: {
    Avatar
  },
  data () {
    return {
      expanded: false
    }
  },
  computed: {
    postContentToShow () {
      if (this.post.text) {
        if (this.post.text.length > 140) {
          if (this.expanded) return this.post.text

          if (!this.expanded) return `${this.post.text.substring(0, 140)}...`
        } else {
          return this.post.text
        }
      }

      return ''
    }
  },
  methods: {
    handlePinPost () {
      this.$emit('pin')
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-board-post {
  margin-top: 20px;
  border-bottom: 1px solid $light-gray;
  &-title {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;

    h3 {
      margin-top: 0;
    }

    ul {
      padding: 0;
      margin: 0;
      list-style: none;
    }
  }

  &:hover {
    .connect-board-post-pin {
      opacity: 1;
    }
  }

  &-info {
    display: flex;

    &-author {
      margin-left: 5px;
      font-size: 13px;
      display: flex;
      flex-direction: column;
      justify-content: space-evenly;
    }

    p {
      margin: 0;
    }
  }

  &-pin {
    opacity: 0;
    cursor: pointer;
    width: 25px;
    height: 25px;
    background-size: cover;
    background-image: url(../../assets/icons/PinLineal.svg);

    &--pinned,
    &:hover {
      opacity: 1;
      background-image: url(../../assets/icons/PinColor.svg);
    }
  }

  &-content {
    margin-bottom: 10px;
  }
}

.expand-post {
  margin-left: 10px;
  img {
    vertical-align: middle;
  }
}
</style>
