<template>
  <v-form>
    <v-slider
        v-model="num_passes"
        label="Number of passes"
        min="0"
        max="50"
        step="1"
        thumb-label="always"
        @change="save"
    ></v-slider>
    <v-slider
        v-model="num_swaps"
        label="Number of swaps"
        min="0"
        max="20"
        step="1"
        thumb-label="always"
        @change="save"
    ></v-slider>
  </v-form>
</template>

<script>
export default {
    data: () => {
        return({
            num_passes: 3,
            num_swaps: 2
        })
    },
  methods: {
    save: function(){
      console.log(this.$data)
      this.$store.commit("setOption", ["postprocessing", this.$data])
    }
  },
  created() {
    this.save()
  }
}
</script>

<style>

</style>