<template>
  <div>
    <div style="padding-bottom:10px">
        <div class="inbox columns">
            <div class="column columns">
                <PuSkeleton style="margin-top:12px" circle height="50px" width="50px"/>
                <div class="column">
                    <PuSkeleton height="20px" width="30%"  />
                    <div>
                        <PuSkeleton height="20px" width="80%"  />
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="items-right">
                    <PuSkeleton  height="20px" width="40px"  />
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
  name: 'InboxSkeleton',
  components: {
      Avatar
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
