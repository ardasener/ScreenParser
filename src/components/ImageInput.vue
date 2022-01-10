<template>
<v-col align="center">
    <v-file-input
        placeholder="Pick image files"
        multiple
        v-model="input_files"
        accept="image/png, image/jpeg"
        prepend-icon="mdi-image"
        label="Local Files"
    ></v-file-input>
<!--    <v-textarea
        v-model="input_urls"
        label="URLs"
        value=""
        hint="Enter an image URL on each line"
    ></v-textarea>-->
    <v-btn @click="load" color="primary">Load</v-btn>
</v-col>
</template>

<script>

const fs = require("fs")
const path = require("path")
const os = require("os")

const home_dir = os.homedir()
const root_dir = path.join(home_dir, "screenparser")

export default {
data: () => {
    return({
        input_files: [],
        input_urls: "",
        input_dir: ""
    })
},
  created() {
    this.input_dir = path.join(root_dir, "inputs")
    fs.mkdirSync(this.input_dir, {recursive: true})
  },
  methods: {
    load: function (){
      console.log("Loading data...")
      fs.rmSync(this.input_dir,{ recursive: true, force: true })
      fs.mkdirSync(this.input_dir, {recursive: true})
      this.input_files.forEach((file, index) => {
        var ext = ".err"
        if(file.type == "image/png"){
          ext = ".png"
        } else if(file.type == "image/jpeg"){
          ext = ".jpeg"
        }
        fs.copyFileSync(file.path, path.join(this.input_dir, "image" + index + ext))
      })

    }
  }
}
</script>

<style>

</style>