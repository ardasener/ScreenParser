import Vuex from 'vuex'
import Vue from "vue";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        options: {
            detection: {
                blur: true,
                rgb_detection: false,
                ocr: true,
                gpu: false,
                selected_langs: ['en'],
                ocr_langs: null,
                ocr_threshold: 0.6,
            },
            filtering: {
                large_obj_threshold: 0.5,
                small_obj_threshold: 0.01,
                intersection_threshold: 0.6,
                text_merge_threshold: 0.01,
                icon_text_merge_threshold: 0.15
            },
            clustering: {
                position_weight: 0.7,
                size_weight: 0.1,
                type_weight: 0.0,
                padding_weight: 0.5,
                clustering_alg: "dbscan",
                dbscan_eps: 0.3,
                dbscan_min_samples: 3,
                ms_quantile: 0.3,
                ms_n_samples: 10
            },
            postprocessing: {
                num_passes: 3,
                num_swaps: 2
            },
        },
        image_dir: "",
        data_dir: "",
        input_files: [],
    },
    mutations: {
        setOption (state, [name, value]) {
            state.options[name] = value
        },
        setImageDir(state, value){
            state.image_dir = value
        },
        setDataDir(state, value){
            state.data_dir = value
        },
        setInputFiles(state,value){
            state.input_files = value
        },
    }
})

export default store;