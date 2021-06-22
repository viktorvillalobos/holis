<template>
  <div class="hover">
    <div class="inbox columns">
        <div class="column columns">
            <!--<Avatar v-if="recent.avatar_thum" class="column" :img="recent.avatar_thumb" :text="recent.name" />-->
            <font-awesome-icon icon="user-circle" size="3x" style="margin-top:10px"/>
            <div class="column">
                <b>{{recent ? recent.name : 'Nombre misterioso' }}</b>
                <div style="color:#828282" v-html="recent.message"></div>
            </div>
        </div>
        <div class="column">
            <div>
                <p style="color:#828282" class="items-right">{{recent.created | moment("hh:mm")}}<p/>
            </div>
            <div class="items-right">
                <font-awesome-icon icon="chevron-right" size="1x" style="color:#828282"/>
            </div>
        </div>
    </div>
    <div class="divider"></div>
  </div>
</template>

<script>
import Avatar from '@/components/Avatar'

export default {
  name: 'InboxMessage',
  components: {
      Avatar
  },
  props:["recent"],
  data () {
    return {}
  }
}
</script>

<style lang="scss">
.inbox{
    height: 100px;
    padding: 30px;
}

.hover{
    padding-top: 10px;
}

.hover:hover{
    cursor: pointer;
    background-color: rgba(128, 128, 128, 0.5);
}

.items-right{
   float: right;
   clear: both;
}

.divider{
    width: 100%;
    height: 0px;
    border:1px solid #F7F7F7
}

</style>
