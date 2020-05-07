<template>
  <div class="connect-releases">
    <release v-for="release in releases" :release="release" :key="release.id" />
  </div>
</template>
<script>
import Release from "./Release";
export default {
  name: "releases",
  components: {
    Release
  },
  data() {
    return {
      releases: [
        {
          id: 1,
          date: "05 de mayo 2020",
          title: "Modo oscuro",
          text: `<div><span class="tag is-primary">Nuevo</span><ul><li><strong></strong><span class="i18n-msg">Disfruta de Paper en el modo oscuro. En cualquier documento, selecciona el icono de pregunta en la esquina inferior derecha de la pantalla y, luego, <b><span class="i18n-msg">Modo oscuro</span></b>.</span></li></ul><span class="tag is-warning">Correcciones</span><ul><li><strong></strong><span class="i18n-msg">Al pegar un vínculo a una lista de reproducción de Spotify en un documento, se mostrará la vista previa de forma correcta.</span></li><li><strong></strong><span class="i18n-msg">Al exportar una línea de tiempo, se mostrarán los elementos ordenados por fecha de inicio en lugar de mostrarse por fecha de creación.</span></li><li><strong></strong><span class="i18n-msg">Al copiar una tarea asignada a otra persona en un documento separado, ya no recibirás (de forma incorrecta) un correo electrónico en el que se te vuelve a asignar la tarea.</span></li><li><strong></strong><span class="i18n-msg">En iOS, al presionar “Crear un documento de tareas” en la pestaña <b><span class="i18n-msg">Tareas pendientes</span></b>, ahora se completará la acción prevista.</span></li></ul></div>`
        },
        {
          id: 2,
          date: "03 de mayo 2020",
          title: "Hello World",
          text: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. <strong>Pellentesque risus mi</strong>, tempus quis placerat ut, porta nec nulla. Vestibulum rhoncus ac ex sit amet fringilla. Nullam gravida purus diam, et dictum <a>felis venenatis</a> efficitur. Aenean ac <em>eleifend lacus</em>, in mollis lectus. Donec sodales, arcu et sollicitudin porttitor, tortor urna tempor ligula, id porttitor mi magna a neque. Donec dui urna, vehicula et sem eget, facilisis sodales sem.`
        },
        {
          id: 3,
          date: "28 de abril 2020",
          title: "Hello World",
          text: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. <strong>Pellentesque risus mi</strong>, tempus quis placerat ut, porta nec nulla. Vestibulum rhoncus ac ex sit amet fringilla. Nullam gravida purus diam, et dictum <a>felis venenatis</a> efficitur. Aenean ac <em>eleifend lacus</em>, in mollis lectus. Donec sodales, arcu et sollicitudin porttitor, tortor urna tempor ligula, id porttitor mi magna a neque. Donec dui urna, vehicula et sem eget, facilisis sodales sem.`
        }
      ]
    };
  }
};
</script>
<style lang="scss" scoped>
.connect-releases {
  padding: 10px;
  height: calc(100vh - 42px);
}
</style>