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
    <v-btn color="primary" @click="save">Save</v-btn>
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