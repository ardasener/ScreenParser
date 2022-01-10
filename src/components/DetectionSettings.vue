<template>
  <v-form>
    <v-switch v-model="blur" label="Apply Blur"></v-switch>
    <v-switch v-model="ocr" label="Use OCR"></v-switch>
    <v-switch v-model="gpu" label="Use GPU for OCR"></v-switch>
    <v-select
      v-model="selected_langs"
      :items="ocr_langs"
      item-text="Name"
      item-value="Code"
      chips
      label="OCR Languages"
      multiple
    ></v-select>
  </v-form>
</template>

<script>
import ocr_langs from "../assets/ocr_langs.json"

export default {
  data: () => {
    return {
      blur: true,
      ocr: true,
      gpu: false,
      selected_langs: ['en'],
      ocr_langs: ocr_langs
    };
  },
};
</script>

<style>
</style>