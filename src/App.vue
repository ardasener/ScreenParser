<template>
  <v-app>
    <v-main>
      <v-stepper non-linear v-model="current_step">
      <v-stepper-header>
        <template v-for="(step,index) in steps">
        <v-stepper-step :key="'step'+index" :step="index+1" editable>
          {{step}}
        </v-stepper-step>
        <v-divider :key="'divide' + index" v-if="index < steps.length-1"></v-divider>
        </template>
      </v-stepper-header>
    </v-stepper>
    <v-row v-if="current_step === 1">
      <image-input class="m-10 p-5"></image-input>
    </v-row>
      <v-row v-if="current_step !== 1 && current_step !== 6">
        <v-col align="center" justify="center" style="max-height: 80%" class="overflow-y-auto">
          <viewer :images="images">
            <img class="m-5" v-for="src in images" :key="src" :src="src" width="60%">
          </viewer>
        </v-col>
        <v-col class="m-10 p-5">
          <detection-settings v-if="current_step === 2"></detection-settings>
          <filtering-settings v-if="current_step === 3"></filtering-settings>
          <clustering-settings v-if="current_step === 4"></clustering-settings>
          <post-processing-settings v-if="current_step === 5"></post-processing-settings>
        </v-col>
      </v-row>
      <v-row align="center" justify="center" class="m-10" v-if="current_step === 6">
        <pre v-highlightjs="xml_output">
          <code class="xml">
          </code>
        </pre>
      </v-row>
    </v-main>
  </v-app>
</template>

<script>
import ClusteringSettings from "./components/ClusteringSettings.vue";
import 'viewerjs/dist/viewer.css'
import VueViewer from 'v-viewer'
import Vue from 'vue'
import DetectionSettings from './components/DetectionSettings.vue';
import FilteringSettings from './components/FilteringSettings.vue';
import PostProcessingSettings from './components/PostProcessingSettings.vue';
import ImageInput from './components/ImageInput.vue';
import 'highlight.js/styles/github.css'


const steps = [
  "Input",
  "Object Detection",
  "Object Filtering",
  "Clustering",
  "Post Processing",
  "Output"
]

Vue.use(VueViewer)
export default {
  name: "App",

  components: {
    ClusteringSettings,
    DetectionSettings,
    FilteringSettings,
    PostProcessingSettings,
    ImageInput,
  },

  data: () => ({
    images: [
      "https://gitlab.com/ardasener/screenparserdata/-/raw/73413ea07349114b01b2a792e5873677f1e141a8/Car/citroen.png",
      "https://gitlab.com/ardasener/screenparserdata/-/raw/main/DSLR/SonyDSLR.png",
      "https://gitlab.com/ardasener/screenparserdata/-/raw/main/Car/honda.png",
      "https://gitlab.com/ardasener/screenparserdata/-/raw/main/DSLR/NikonDSLR2.png",
      "https://dappgrid.com/wp-content/uploads/2020/12/connect-metamask-to-uniswap.jpg",
      "https://uploads.golmedia.net/uploads/articles/article_media/2485111481606160997gol1.jpg",
    ],
    steps: steps,
    current_step: 1,
    xml_output: "<Hello><World></World></Hello>"
  }),
};
</script>
