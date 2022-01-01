<template>
  <v-form>
    <v-slider
        v-model="num_passes"
        label="Number of passes"
        min="0"
        max="50"
        step="1"
        thumb-label="always"
    ></v-slider>
    <v-slider
        v-model="num_swaps"
        label="Number of swaps"
        min="0"
        max="20"
        step="1"
        thumb-label="always"
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
    }
}
</script>

<style>

</style>