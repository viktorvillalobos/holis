<template>
  <div>
    <CreateGroup />
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
    return {}
  },
}
</script>

<style lang="scss">
</style>
