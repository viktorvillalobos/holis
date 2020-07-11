<template>
  <div class="connect-WIP">
    <img
      src="https://media1.tenor.com/images/6003bca7cb79d72d9deb2500933ddca8/tenor.gif?itemid=14473694"
      alt="CAT Working"
    />
    <h4>Ah, pérame que estoy trabajando en esto...</h4>
  </div>
</template>
<script>
export default {
  name: 'WIP'
}
</script>
<style lang="scss" scoped>
.connect-WIP {
    widows: 100%;
    display: flex;
    flex-direction: column;
    vertical-align: center;
    align-items: center;
    justify-content: center;
    padding: 10px;

    img {
        max-width: 300px;
    }

    h4 {
        margin-top: 15px;
    }
}
</style>
