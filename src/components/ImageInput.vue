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
    <v-textarea
        v-model="input_urls"
        label="URLs"
        value=""
        hint="Enter an image URL on each line"
    ></v-textarea>
    <v-btn color="primary">Load</v-btn>
</v-col>
</template>

<script>
export default {
data: () => {
    return({
        input_files: [],
        input_urls: "",
    })
}
}
</script>

<style>

</style>