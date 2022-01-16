<template>
  <v-app>
    <v-main>
      <v-stepper non-linear v-model="current_step" v-if="input_files.length !== 0">
        <v-stepper-header>
          <template v-for="(step,index) in steps">
            <v-stepper-step :key="'step'+index" :step="index+1" editable>
              {{ step }}
            </v-stepper-step>
            <v-divider :key="'divide' + index" v-if="index < steps.length-1"></v-divider>
          </template>
        </v-stepper-header>
      </v-stepper>
      <v-row v-show="current_step === 1">
        <v-file-input
            placeholder="Pick image files"
            multiple
            v-model="input_files"
            accept="image/png, image/jpeg"
            prepend-icon="mdi-image"
            label="Local Files"
            class="m-5"
            @change="load_files"
        ></v-file-input>
      </v-row>
      <v-row v-show="current_step !== 1 && current_step !== 6">
        <v-col align="center" justify="center" >
          <v-card   elevation="2"
                    class="overflow-y-auto m-10" height="70vh" justify="center" align="center">
            <viewer :images="images()">
              <img class="m-5" v-for="src in images()" :key="src" :src="src" width="60%">
            </viewer>
          </v-card>
        </v-col>
        <v-col class="m-10 p-5">
          <detection-settings v-show="current_step === 2"></detection-settings>
          <filtering-settings v-show="current_step === 3"></filtering-settings>
          <clustering-settings v-show="current_step === 4"></clustering-settings>
          <post-processing-settings v-show="current_step === 5"></post-processing-settings>
        </v-col>
      </v-row>
      <v-row align="center" justify="center" class="m-10" v-if="current_step === 6">
        <v-form class="m-5">
          <v-btn class="m-2" @click="show_data"><v-icon left>mdi-code-tags</v-icon>Show Output Folder</v-btn>
          <v-btn class="m-2" @click="show_images"><v-icon left>mdi-image</v-icon>Show Images Folder</v-btn>
        </v-form>
      </v-row>
      <runner @runFinished="rerender"></runner>
      <setup v-if="setup" @setupDone="setup = false"></setup>
    </v-main>
  </v-app>
</template>

<script>
import ClusteringSettings from "./components/ClusteringSettings.vue";
import DetectionSettings from './components/DetectionSettings.vue';
import FilteringSettings from './components/FilteringSettings.vue';
import PostProcessingSettings from './components/PostProcessingSettings.vue';
import Setup from './components/Setup.vue'
import Runner from "./components/Runner.vue";


const fs = require("fs")
const path = require("path")
const {shell} = require('electron')

const steps = [
  "Input",
  "Object Detection",
  "Object Filtering",
  "Clustering",
  "Post Processing",
  "Output"
]

export default {
  name: "App",

  components: {
    Runner,
    ClusteringSettings,
    DetectionSettings,
    FilteringSettings,
    PostProcessingSettings,
    Setup,
  },

  data: () => ({
    input_files: [],
    steps: steps,
    current_step: 1,
    setup : true,
    current_output: 0,
  }),
  mounted() {
    this.$vuetify.theme.dark = true
  },
  computed: {},
  methods: {
    load_files: function(){
      console.log()
      const paths = this.input_files.map((file) => {return file.path})
      this.$store.commit("setInputFiles", paths)
    },
    rerender: function (){
      console.log("Rerendering...")
      this.$forceUpdate()
    },
    images: function (){
      var filter_word = ""

      if(this.current_step === 2){
        filter_word = "detection"
      } else if(this.current_step  === 3){
        filter_word = "filtering"
      } else if(this.current_step  === 4){
        filter_word = "clustering"
      } else if(this.current_step  === 5){
        filter_word = "final"
      } else {
        return []
      }

      const image_dir = this.$store.state.image_dir
      const images = fs.readdirSync(image_dir)

      const filtered = images.filter((image) => {return image.includes(filter_word)}).map((image) =>
      {return "local-resource://"+path.join(image_dir, image)})
      filtered.sort()
      console.log(filtered)
      return filtered
    },
    show_data: function (){
      console.log(this.$store.state.data_dir)
      shell.openPath(this.$store.state.data_dir)
    },
    show_images: function (){
      console.log(this.$store.state.image_dir)
      shell.openPath(this.$store.state.image_dir)
    }
  }
};
</script>
