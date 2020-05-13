<template>
  <div class="connect-searcher-container">
    <div class="field">
      <p class="control has-icons-left has-icons-right is-loading">
        <input class="input" placeholder="Busca a una persona..." />
        <span class="icon is-small is-left">
          <i class="fas fa-envelope"></i>
        </span>
        <span class="icon is-small is-right">
          <font-awesome-icon icon="search" />
        </span>
      </p>
    </div>
    <Btn primary icon>
      <font-awesome-icon icon="street-view" />
    </Btn>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
export default {
  name: "Searcher",
  components: { Btn }
};
</script>
<style lang="scss" scoped>
.connect-searcher-container {
  position: fixed;
}
</style>