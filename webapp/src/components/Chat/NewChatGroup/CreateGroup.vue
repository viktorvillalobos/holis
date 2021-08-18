<template>
    <div class="new-chat">
        <div class="header-new-chat columns pt-5 flx-1">
            <button class="button is-ghost column is-1" @click="backComponent">
                <span class="icon is-small">
                    <span class="material-icons" style="color:#fff">chevron_left</span>
                </span>
            </button>
            <b class="column" style="color:#fff">New group</b>
        </div>
        
        <div class="is-flex is-justify-content-center">
            <input class="file-input" type="file" id="fileUpload" accept="image/*" @change="previewFiles" hidden>
            <figure class="image is-128x128" v-if="url" @click="chooseFiles">
                <img class="is-rounded" :src="url">
            </figure>
            <figure v-else class="circle is-flex is-justify-content-center is-clickable" @click="chooseFiles">
                <span class="material-icons mt-6" style="color: white; font-size: 32px">
                    perm_media
                </span>
            </figure>
        </div>

        <div class="field mr-5 ml-5 mt-5 flx-1">
            <input class="input" type="text" placeholder="Group name" v-model="group">
        </div>
        <div class="flx-1 m-5">
            <button class="button is-fullwidth is-primary">Select participants</button>
        </div>
    </div>
</template>

<script>

export default {
  name: 'CreateChatGroup',
  data () {
    return {
      group: "",
      url: ""
    }
  },
  components: {},
  methods:{
    backComponent(){
    },
    chooseFiles() {
        document.getElementById("fileUpload").click()
    },
    previewFiles(event) {
      const file = event.target.files[0];
      this.url = URL.createObjectURL(file);
    }
  },
}
</script>

<style lang="scss">
.new-chat{
  display: flex;
  flex-direction: column;
  height: 100%;

  &-flx-1{
    flex: 1;
  }

  &-flx-0{
    flex: 0;
  }
}

.header-new-chat {
  font-family: $family-dm-sans;
  background: #364DFF;
  margin-left: 0px !important;
  padding-left: 0px;
  height: 90px;
  //background: linear-gradient(90deg, #364DFF 0%, #5165FF 100%);
  box-shadow: 0px 4px 4px rgba(224, 224, 224, 0.1);

    &-title{
        max-lines: 1;
        margin-left:20px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 1; /* number of lines to show */
        -webkit-box-orient: vertical;
    }
}

.user-items{
    padding: 20px 40px 20px 40px;
}

.user-items:hover{
    cursor: pointer;
    background-color: rgba(128, 128, 128, 0.5);
}

.circle{
    border-radius: 50%;
    width: 128px;
    height: 128px; 
    background: $primary;
}

</style>
