<template>
  <v-form>
    <v-slider
      v-model="position_weight"
      label="Position Weight"
      min="0"
      max="1"
      step="0.1"
      thumb-label="always"
    ></v-slider>
    <v-slider
      v-model="size_weight"
      label="Size Weight"
      min="0"
      max="1"
      step="0.1"
      thumb-label="always"
    ></v-slider>
    <v-slider
      v-model="type_weight"
      label="Object Type Weight"
      min="0"
      max="1"
      step="0.1"
      thumb-label="always"
    ></v-slider>
    <v-slider
      v-model="padding_weight"
      label="Padding Weight"
      min="0"
      max="1"
      step="0.1"
      thumb-label="always"
    ></v-slider>
    <v-radio-group v-model="clustering_alg" row>
      <v-radio label="DBScan" value="dbscan"></v-radio>
      <v-radio label="MeanShift" value="meanshift"></v-radio>
    </v-radio-group>
     <v-slider
      v-model="dbscan_eps"
      v-if="clustering_alg === 'dbscan'"
      label="Eps"
      min="0"
      max="1"
      step="0.05"
      thumb-label="always"
    ></v-slider>
    <v-slider
      v-model="dbscan_min_samples"
      v-if="clustering_alg === 'dbscan'"
      label="Min Samples"
      min="1"
      max="100"
      step="1"
      thumb-label="always"
    ></v-slider>
    <v-slider
      v-model="ms_quantile"
      v-if="clustering_alg === 'meanshift'"
      label="Quantile"
      min="0"
      max="1"
      step="0.05"
      thumb-label="always"
    ></v-slider>
    <v-slider
      v-model="ms_n_samples"
      v-if="clustering_alg === 'meanshift'"
      label="Number of Samples"
      min="1"
      max="100"
      step="1"
      thumb-label="always"
    ></v-slider>


  </v-form>
</template>

<script>
export default {
  data: () => {
    return {
      position_weight: 0.7,
      size_weight: 0.1,
      type_weight: 0.0,
      padding_weight: 0.5,
      clustering_alg: "dbscan",
      dbscan_eps: 0.3,
      dbscan_min_samples: 3,
      ms_quantile: 0.3,
      ms_n_samples: 10
    };
  },
};
</script>

<style>
</style>