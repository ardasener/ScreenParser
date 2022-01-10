<template>
  <v-btn @click="run">
    <v-icon>
      {{icon}}
    </v-icon>
  </v-btn>
</template>

<script>

const fs = require('fs')
const os = require('os')
const path = require('path')
const { exec } = require("child_process");
const https = require('https');


export default {
  data: () => {
    return ({
      data_dir: "",
      image_dir: "",
      root_dir: "",
      env_path: "",
      pip_path: "",
      python_path: "",
      input_dir: "",
      status: "working",
    })
  },
  created() {
    const home_dir = os.homedir();
    this.root_dir = path.join(home_dir, "screenparser")
    this.data_dir = path.join(home_dir, "screenparser", "data")
    this.image_dir = path.join(home_dir, "screenparser", "images")
    this.env_path = path.join(this.root_dir,"env")
    this.pip_path = path.join(this.env_path,"bin","pip")
    this.python_path = path.join(this.env_path,"bin","python")
    this.input_dir = path.join(this.root_dir, "inputs")
    fs.mkdirSync(this.data_dir, {recursive: true})
    fs.mkdirSync(this.image_dir, {recursive: true})

    console.log("Creating environment...");
    exec("python3.7 -m venv " + this.env_path, (error, stdout, stderr) => {
      if(error){
        console.log(error.message)
        console.log(stderr)
        this.status = "error"
      } else {
        console.log("Installing dependencies...");
        exec(this.pip_path + " install easyocr opencv-python scikit-learn", {cwd: this.root_dir}, (error, stdout, stderr) => {
          if(error){
            console.log(error.message)
            console.log(stderr)
            this.status = "error"
          } else {
            https.get("https://gist.githubusercontent.com/ardasener/e7c1240532258a7d8b914dc5fe05e5d8/raw/56d4f4afd3f0e42ed4b08dd39276c492ac39bdc8/screenparser.py",(res) => {
              // Image will be stored at this path
              this.script_path = path.join(this.env_path, "screenparser.py")
              const filePath = fs.createWriteStream(this.script_path);
              res.pipe(filePath);
              filePath.on('finish',() => {
                filePath.close();
                console.log('Download Completed');
                this.status = "idle"
              })
            })
          }
        })
      }
    })

  },
  methods: {
    run: function (){
      console.log("Running python script")
      this.status = "working"
      const inputs = fs.readdirSync(this.input_dir)
      console.log(inputs)
      inputs.forEach((file) => {
        const full_path = path.join(this.input_dir, file)
        console.log(this.python_path + " " + this.script_path + " " + full_path + " " + this.data_dir + " " + this.image_dir)
        exec(this.python_path + " " + this.script_path + " " + full_path + " " + this.data_dir + " " + this.image_dir, (error, stderr, stdout) => {
          if(error){
            console.log(error)
            console.log(stderr)
          } else {
            console.log(stdout)
            this.status = "idle"
          }
        })
      })
    }
  },
  computed: {
    icon: function (){
      if(this.status === "working"){
        return "mdi-timer-sand-empty"
      } else if (this.status === "idle") {
        return "mdi-play-box-outline"
      } else {
        return "mdi-alert"
      }
    }
  }
}
</script>