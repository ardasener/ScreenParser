<template>
  <v-dialog
    value="dialog"
    width="500" >
    <v-form class="m-3">
      <v-text-field label="Python Executable" v-model="python_exe"></v-text-field>
      <v-btn color="primary" @click="setup">Setup</v-btn>
      <v-alert v-if="status !== ''" icon="mdi-timer-sand-empty" class="m-3" width="70%">
        {{status}}
      </v-alert>
    </v-form>
  </v-dialog>
</template>

<script>
const path = require("path")
const {exec} = require("child_process")
import axios from 'axios';


const root_path = ".";
const backend_path = path.join(root_path, "backend")
const requirements_path = path.join(backend_path, "requirements.txt")
const app_path = path.join(backend_path, "app.py")

export default {
  mounted() {
    axios.get("http://127.0.0.1:5111/hello").then((response) => {
      console.log(response)
      this.$emit("setupDone")
    }).catch((error) => {
      console.log(error)
      this.dialog = true
    })
  },
  data: () => {
    return({
      python_exe: "python",
      status: "",
      dialog: false,
      error: false,
    })
  },
  methods: {
    setup: function (){
      console.log("Installing Dependencies...")
      this.status = "Installing Dependencies..."
      exec(this.python_exe + " -m pip install -r " + requirements_path, error => {
        if(error){
          console.log(error)
          this.status = "An error occurred"
          this.error = true
          return
        }

        console.log("Starting Backend...")
        exec(this.python_exe + " " + app_path, error => {
          if(error){
            console.log(error)
            this.status = "An error occurred"
            this.error = true
            return
          }
        })

        setTimeout(() => {
          if(!this.error){
            this.$emit("setupDone")
          }
        }, 3000);
      })
    }
  }
}
</script>