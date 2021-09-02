<template>
  <div class="hover">
    <div style="padding-bottom:10px">
        <div class="inbox columns">
            <div class="column columns">
                <Avatar v-if="myRecent && myRecent.image" :img="myRecent.image" style="margin-top:12px"/>
                <font-awesome-icon v-else icon="user-circle" size="3x" style="margin-top:12px"/>
                <div class="column">
                    <b class="inbox-title">{{myRecent ? myRecent.name : 'Nombre misterioso' }}</b>
                    <div :class="{'inbox-message': true, 'inbox-message-active': have_unread_messages }">{{ myRecent && myRecent.last_message_text ? myRecent.last_message_text : "Write the first message" }}</div>
                </div>
            </div>
            <div class="column">
                <div>
                  <p v-if="myRecent" style="color:#828282" class="items-right">{{ myRecent.last_message_ts | moment("hh:mm")}}</p>
                  <p v-else style="color:#828282" class="items-right"></p>
                </div>
                <div class="items-right">
                    <font-awesome-icon icon="chevron-right" size="1x" style="color:#828282"/>
                </div>
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
  props: {
    recent: {
      type: Object,
      default: {}
    }
  },
  computed: {
    have_unread_messages () {
      return this.recent && this.recent.have_unread_messages
    },
    myRecent () {
      return this.recent
    }
  },
  data () {
    return {}
  }
}
</script>

<style lang="scss">
.inbox{
    font-family: $family-dm-sans;
    height: 100px;
    padding: 20px 40px 20px 50px;

    &-title{
        font-size: 16px;
        color:#000000;
    }

    &-message{
        font-size: 14px;
        margin-top: 2px;
        color:#828282;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 1; /* number of lines to show */
        -webkit-box-orient: vertical;

        &-active{
            color:$primary;
            font-weight:bold;
        }
    }
}

.hover{
    padding-top: 10px;
    padding-right: 12px;
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
    border:1px solid #F7F7F7;
    margin-left: 6px;
}

</style>
