<template>
  <div class="holis-config-voice-video">
    <div class="columns">
      <div class="column">
        <div class="field">
          <label for class="label">Input devices</label>
          <div class="select is-fullwidth is-small">
            <select  @change="handleDeviceChange($event, 'audioinput')">
              <option v-for="device in inputDevices"
                      :selected="device.deviceId == selectedInputDevice"
                      :key="device.deviceId"
                      :value="device.deviceId"> {{ device.label }}</option>
            </select>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <label for class="label">Output devices</label>
          <div class="select is-fullwidth is-small">
            <select @change="handleDeviceChange($event, 'audiooutput')">
              <option v-for="device in outputDevices"
                      :key="device.deviceId"
                      :value="device.deviceId"
              > {{ device.label }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <div class="field">
          <label for class="label">Input volume</label>
          <input
            class="slider is-fullwidth is-success"
            step="1"
            min="0"
            max="150"
            type="range"
            v-model="inputVolume"
          />
          <output for="sliderWithValue">{{inputVolume}}</output>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <label for class="label">Output volume</label>
          <input
            id="sliderWithValue"
            v-model="outputVolume"
            min="0"
            max="150"
            step="1"
            type="range"
          />
          <output for="sliderWithValue">{{outputVolume}}</output>
        </div>
      </div>
    </div>
    <ul class="card-actions">
      <li>
        <Btn primary>Save</Btn>
      </li>
    </ul>
  </div>
</template>

<script>
import Btn from '@/components/Btn'
export default {
  name: 'VoiceAndVideo',
  components: { Btn },
  data () {
    return {
      inputVolume: 100,
      outputVolume: 100,
      inputDevices: [],
      outputDevices: [],
      selectedInputDevice: null,
      selectedOutputDevice: null
    }
  },
  async created () {
    await this.getDevices()
    this.loadDevicesFromLocalStorage()
  },
  methods: {
    async getDevices () {
      const devices = await navigator.mediaDevices.enumerateDevices()
      this.inputDevices = devices.filter(device => device.kind === 'audioinput')
      this.outputDevices = devices.filter(device => device.kind === 'audiooutput')
    },
    loadDevicesFromLocalStorage () {
      const inputDeviceId = window.localStorage.getItem('inputDeviceId')
      const outputDeviceId = window.localStorage.getItem('outputDeviceId')
      this.selectedInputDevice = this.inputDevices.filter(device => device.deviceId === inputDeviceId)[0]
      this.selectedOutputDevice = this.outputDevices.filter(device => device.deviceId === outputDeviceId)[0]
    },
    handleDeviceChange (event, kind) {
      const selectedDeviceId = event.target.value
      if (kind === 'audioinput') {
        window.localStorage.setItem('inputDeviceId', selectedDeviceId)
        this.selectedInputDevice = selectedDeviceId
      }

      if (kind === 'audiooutput') {
        window.localStorage.setItem('outputDeviceId', selectedDeviceId)
        this.selectedOutputDevice = selectedDeviceId
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
