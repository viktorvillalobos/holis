<template>
  <div class="card ml-4 mb-3">
        <div class="card-content">
            <div class="media">
                <div class="media-content">
                    <div>
                        <PuSkeleton height="20px" width="70%"  />
                    </div>
                    <div>
                        <PuSkeleton width="30%"/>
                    </div>
                    <div>
                        <PuSkeleton width="30%" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Card from '@/components/Card'
import Btn from '@/components/Btn'
export default {
  name: 'ProjectSkeleton',
  components: {
    Card,
    Btn
  },
}
</script>
<style lang="scss" scoped>
</style>
