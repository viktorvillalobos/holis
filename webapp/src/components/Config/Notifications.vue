<template>
  <div class="holis-config-notifications">
    <div class="header">
      <h3 class="header-title">
        <span class="material-icons header-icon has-text-primary">groups</span>
        Notifications
      </h3>
    </div>

    <div class="container">
      <div class="field field-switch">
        <label for="switchRoundedDefault">Permitir notificaciones de escritorio</label>
        <input
          id="switchRoundedDefault"
          type="checkbox"
          name="switchRoundedDefault"
          class="switch is-rounded"
          checked="checked"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Notifications'
}
</script>

<style lang="scss" scoped>
</style>
