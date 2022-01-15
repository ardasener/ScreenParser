<template>
  <div>
    <v-btn :color="btn_color" fab
           bottom
           right
           absolute
           class="my-10 mx-5"
           @click="btn_click"
    >
      <v-icon class="px-5">
        {{btn_icon}}
      </v-icon>
    </v-btn>

    <v-snackbar
        v-model="snackbar"
    >
      {{ error_msg }}
      <template v-slot:action="{ attrs }">
        <v-btn
            color="red"
            text
            v-bind="attrs"
            @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>

  </div>
</template>

<script>

import axios from 'axios';


export default {
  data: () => {
    return({
      status: "idle",
      error_msg: "",
      snackbar: false,
    })
  },
  methods: {
    btn_click: function() {
      if(this.status === "idle"){
        this.status = "working"

        axios.post("http://127.0.0.1:5000/run", {input_files: this.$store.state.input_files, options: this.$store.state.options})
            .then((response) => {
              this.status = "idle"
              console.log(response)
              this.$store.commit("setImageDir", response.data.image_dir)
              this.$store.commit("setDataDir", response.data.data_dir)
              this.$emit('runFinished')
            })
            .catch((error) => {
              this.status = "error"
              this.error_msg = error.toString()
              if(this.error_msg === "")
                this.error_msg = "An error occurred!"
              console.log(error.toString())
              this.$emit('runFinished')
            });
      } else if (this.status === "error"){
        this.snackbar = true
        this.status = "idle"
      } else if (this.status === "working"){
        this.snackbar = true
        this.error_msg = "Still processing. Please be patient."
      }
    }
  },
  computed: {
    btn_icon: function() {
      if(this.status === "idle")
        return "mdi-play-circle"
      else if(this.status === "working")
        return "mdi-timelapse"
      else
        return "mdi-alert-circle"
    },
    btn_color: function(){
      if(this.status === "idle")
        return "success"
      else if(this.status === "working")
        return "secondary"
      else
        return "error"
    }
  }
}
</script>