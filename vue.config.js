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
            to: "backend",
            filter: ["**/*"]
          }
        ]
      }
    }
  }
}
