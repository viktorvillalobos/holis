<template>
  <div class="card m-2">
        <div class="card-content">
            <div class="media">
                <div class="media-left">
                    <figure class="image is-48x48">
                    <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image">
                    </figure>
                </div>
                <div class="media-content">
                    <p class="is-size-7">Hexagonal interactivo</p>
                    <p class="is-size-7">Equipo: Juanin Juan Harry, Tulio Triviño.</p>
                </div>

                <div class="media-right" align="right">
                    <p class="is-size-7">Fecha final: 15 de Febrero 2021</p>
                    <div>
                        <button class="button is-danger is-light is-small alert-days">15 tareas abiertas</button>
                        <button class="button is-success is-light is-small alert-days">15 días restantes</button>
                    </div>
                    <div>
                        <button class="button is-danger is-inverted is-small">Borrar</button>
                        <button class="button is-primary is-inverted is-small">Editar</button>
                        <button class="button is-primary is-inverted is-small">Ver más</button>
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
  name: 'Project',
  props: ["project"],
  components: {
    Card,
    Btn
  },
}
</script>
<style lang="scss" scoped>
.alert-days{
    padding: 2px;
    margin-left: 5px;
}
</style>
