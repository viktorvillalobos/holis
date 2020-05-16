<template>
  <article class="message release-message">
    <div class="message-header">
      <p>
        <span class="message-date">{{release.created | moment('DD/MM/YYYY')}}</span>
        {{release.title}}
      </p>
    </div>
    <div class="message-body" v-html="release.text"></div>
  </article>
</template>
<script>
export default {
  name: "Release",
  props: {
    release: {
      type: Object
    }
  }
};
</script>
<style lang="scss">
.message {
  &-date {
    display: block;
    font-size: 0.8rem;
    margin-bottom: 5px;
  }

  &-header {
    background-color: $light-gray !important;
    color: $font-color !important;
  }

  &-body {
    border: 1px solid $light-gray !important;
    border-top: transparent;
    ul {
        margin-bottom: 15px;
        padding-left: 15px;
        list-style: disc;
    }
  }
}
</style>