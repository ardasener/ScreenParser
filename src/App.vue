<template>
  <v-app>
    <v-main>
      <v-stepper non-linear v-model="current_step">
        <v-row>
          <v-col cols="2">
            <python-runner></python-runner>
          </v-col>

          <v-col cols="22">
            <v-stepper-header>
              <template v-for="(step,index) in steps">
                <v-stepper-step :key="'step'+index" :step="index+1" editable>
                  {{ step }}
                </v-stepper-step>
                <v-divider :key="'divide' + index" v-if="index < steps.length-1"></v-divider>
              </template>
            </v-stepper-header>
          </v-col>
        </v-row>
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
import PythonRunner from "./components/PythonRunner";
import os from "os";
import path from "path";

const fs = require("fs")

const home_dir = os.homedir()
const root_dir = path.join(home_dir, "screenparser")
const image_dir = path.join(root_dir, "images")

const steps = [
  "Input",
  "Object Detection",
  "Object Filtering",
  "Clustering",
  "Post Processing",
  "Output",
  "PythonRunner"
]

Vue.use(VueViewer)
export default {
  name: "App",

  components: {
    PythonRunner,
    ClusteringSettings,
    DetectionSettings,
    FilteringSettings,
    PostProcessingSettings,
    ImageInput,
  },

  data: () => ({
    steps: steps,
    current_step: 1,
    xml_output: "<Hello><World></World></Hello>"
  }),
  mounted() {
    this.$vuetify.theme.dark = true
  },
  computed: {
    images: function (){
      var files = fs.readdirSync(image_dir)
      console.log(files)
      return files
    }
  }
};
</script>
