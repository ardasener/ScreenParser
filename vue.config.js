module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        extraFiles: [
          {
            from: "backend",
            to: "./resources/app.asar.unpacked/backend",
            filter: ["**/*"]
          }
        ]
      }
    }
  }
}
