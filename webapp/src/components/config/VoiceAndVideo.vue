<template>
  <div class="holis-config-voice-video">
    <div class="columns">
      <div class="column">
        <div class="field">
          <label for class="label">Dispositivo de entrada</label>
          <div class="select is-fullwidth is-small">
            <select>
              <option>Select dropdown</option>
              <option>With options</option>
            </select>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <label for class="label">Dispositivo de salida</label>
          <div class="select is-fullwidth is-small">
            <select>
              <option>Select dropdown</option>
              <option>With options</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <div class="field">
          <label for class="label">Volumen de entrada</label>
          <input
            class="slider is-fullwidth is-success"
            step="1"
            min="0"
            max="150"
            type="range"
            v-model="instance.inputVolume"
          />
          <output for="sliderWithValue">{{instance.inputVolume}}</output>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <label for class="label">Volumen de salida</label>
          <input
            id="sliderWithValue"
            v-model="instance.outputVolume"
            min="0"
            max="150"
            step="1"
            type="range"
          />
          <output for="sliderWithValue">{{instance.outputVolume}}</output>
        </div>
      </div>
    </div>
    <ul class="card-actions">
      <li>
        <Btn primary>Guardar</Btn>
      </li>
    </ul>
  </div>
</template>

<script>
import Btn from "@/components/Btn";
export default {
  name: "VoiceAndVideo",
  components: { Btn },
  data: () => ({
    instance: {
      inputVolume: 100,
      outputVolume: 100,
    },
  }),
  created() {
    bulmaSlider.attach();
  },
};
</script>

<style lang="scss" scoped>
</style>