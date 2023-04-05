<template>
    <v-snackbar :timeout="3000" multi-line v-model="snackbarShow.is">
        {{ snackbarShow.msg }}
    </v-snackbar>
    <v-tabs v-model="tab" centered grow color="primary">
        <v-tab value="calculate">计算</v-tab>
        <v-tab value="predicted">预测</v-tab>
        <v-tab value="readme">说明</v-tab>
    </v-tabs>
    <v-window v-model="tab">
        <v-window-item value="calculate">
            <v-container>
            </v-container>
        </v-window-item>
        <v-window-item value="predicted">
            <v-container>
            </v-container>
        </v-window-item>
    </v-window>
</template>
<script setup>
import { reactive, ref } from 'vue';
import _ from "lodash";
const snackbarShow = ref({ is: false, msg: "" })
const tab = ref("predicted")
let data = reactive({
    inputTab: [],
    result: {},
})

function addItem(idxs) {
    data.group.push(_.cloneDeep(data.group[idxs]))
}
function reduceItem(idxs) {
    if (idxs != 0) {
        data.group.splice(idxs, 1)
    }
    else {
        snackbarShow.value.msg = '至少保留一个'
        snackbarShow.value.is = true
    }
}




</script>
<style scoped>
:deep(.v-text-field .v-field--active input) {
    text-align: center;
}
</style>