<template>
  <div>
    <CreateGroup v-if="screen == 'index'" @send="updateScreen"/>
    <CreateGroupParticipants v-else @send="updateScreen" />
  </div>
</template>

<script>

import CreateGroup from "./CreateGroup"
import CreateGroupParticipants from "./CreateGroupParticipants"

export default {
  name: 'ChatGroup',
  components:{
    CreateGroup,
    CreateGroupParticipants
  },
  data () {
    return {
      screen: 'index'
    }
  },
  methods:{
    updateScreen(screen) {
        this.screen = screen
    }
  }
}
</script>

<style lang="scss">
</style>
