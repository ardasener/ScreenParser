<template>
    <v-form>
        <v-slider
            v-model="large_obj_threshold"
            label="Large Object Threshold"
            min="0"
            max="1"
            step="0.1"
            thumb-label="always"
        ></v-slider>
        <v-slider
            v-model="small_obj_threshold"
            label="Small Object Threshold"
            min="0"
            max="0.1"
            step="0.01"
            thumb-label="always"
        ></v-slider>
        <v-slider
            v-model="intersection_threshold"
            label="Intersection Threshold"
            min="0"
            max="1"
            step="0.1"
            thumb-label="always"
        ></v-slider>
        <v-slider
            v-model="text_merge_threshold"
            label="Text Merge Threshold"
            min="0"
            max="1"
            step="0.01"
            thumb-label="always"
        ></v-slider>
        <v-slider
            v-model="icon_text_merge_threshold"
            label="Icon/Text Merge Threshold"
            min="0"
            max="1"
            step="0.01"
            thumb-label="always"
        ></v-slider>
    </v-form>
</template>

<script>
export default {
    data: () => {
        return({
            large_obj_threshold: 0.5,
            small_obj_threshold: 0.01,
            intersection_threshold: 0.6,
            text_merge_threshold: 0.01,
            icon_text_merge_threshold: 0.15
                
        })
    }
}
</script>

<style>

</style>