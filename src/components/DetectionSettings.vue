<template>
  <v-form>
    <v-switch v-model="blur" label="Apply Blur" @change="save"></v-switch>
    <v-switch v-model="rgb_detection" label="Use RGB Detection" @change="save"></v-switch>
    <v-switch v-model="ocr" label="Use OCR" @change="save"></v-switch>
    <v-switch v-model="gpu" label="Use GPU for OCR" @change="save"></v-switch>
    <v-select
      v-model="selected_langs"
      :items="ocr_langs"
      item-text="Name"
      item-value="Code"
      chips
      label="OCR Languages"
      multiple
      @change="save"
    ></v-select>
    <v-slider
        v-model="ocr_threshold"
        label="OCR Confidence Threshold"
        min="0"
        max="1"
        step="0.05"
        thumb-label="always"
        @change="save"
    ></v-slider>
  </v-form>
</template>

<script>
import ocr_langs from "../assets/ocr_langs.json"

export default {
  data: () => {
    return {
      blur: true,
      rgb_detection: false,
      ocr: true,
      gpu: false,
      selected_langs: ['en'],
      ocr_langs: ocr_langs,
      ocr_threshold: 0.6,
    };
  },
  methods: {
    save: function(){
      console.log(this.$data)
      this.$store.commit("setOption", ["detection", this.$data])
    }
  },
  created() {
    this.save()
  }
};
</script>

<style>
</style>