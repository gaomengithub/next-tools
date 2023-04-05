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
                <v-card v-for="(items, idxs) in data.group" :key="idxs" class="mb-3">
                    <v-card-title>
                        第{{ idxs + 1 }}组
                    </v-card-title>
                    <Calculate :parentData="items"></Calculate>
                    <v-card-actions>
                        <v-btn @click="addItem(idxs)">增加一组</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn @click="reduceItem(idxs)">删除该组</v-btn>
                    </v-card-actions>
                </v-card>
            </v-container>
        </v-window-item>
        <v-window-item value="predicted">
            <v-container>
            <v-card v-for="(items, idxs) in data.group" :key="idxs" class="mb-3">
                    <v-card-title>
                        第{{ idxs + 1 }}组
                    </v-card-title>
                    <Calculate :parentData="items">
                        <Predicted :parentData="items"></Predicted>
                    </Calculate>
                    <v-card-actions>
                        <v-btn @click="addItem(idxs)">增加一组</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn @click="reduceItem(idxs)">删除该组</v-btn>
                    </v-card-actions>
                </v-card>
            </v-container>            
        </v-window-item>
    </v-window>
</template>
<script setup>
import { reactive, ref } from 'vue';
import _ from "lodash";
import Calculate from './Calculate.vue';
import Predicted from './Predicted.vue';
const snackbarShow = ref({ is: false, msg: "" })
const tab = ref("predicted")
let data = reactive({
    group: [
        {
            chart: [
                [3, 5, 6, 5, 3],
                [3, 8, 3, 5, 3],
                [6, 7, 2, 3, 4],
                [4, 3, 7, 2, 6],
            ],
            chartSum: [22, 22, 22, 22],
            numbers: 22,
            perfix: "C",
            diff: [0, 0, 0, 0],
            ship: [],
            weight: [0.250, 0.250, 0.250, 0.250],
            matx: [],
            indicatorItems:[3, 3, 3, 3],
        },
    ],
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