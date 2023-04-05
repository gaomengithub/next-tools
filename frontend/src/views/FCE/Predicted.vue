<template>
    <Loader ref="loader"></Loader>
    <v-snackbar :timeout="3000" multi-line v-model="snackbarShow.is">
        {{ snackbarShow.msg }}
    </v-snackbar>
    <v-card-text class="d-flex align-end  flex-row">
        <v-sheet class="text-h6">
            第一步，确定人数：
        </v-sheet>
        <v-sheet class="w-50">
            <v-text-field class="w-50" v-model.number="data.numbers" placeholder="专家数量" variant="underlined"
                hide-details="auto">
            </v-text-field>
        </v-sheet>
    </v-card-text>
    <v-card-title>
        第二步，依次确定指标数量和指标的基准：
    </v-card-title>
    <v-card-text class="pb-1">
        <v-container>
            <div class="d-flex align-start justify-space-between flex-row" v-for="(_, idx) in data.indicatorItems">
                <v-sheet>
                    <span class="text-h6 ">
                        {{ idx + 1 }}
                    </span>
                </v-sheet>
                <v-sheet style="width: 80%;">
                    <v-slider v-model="data.indicatorItems[idx]" :ticks="tickLabels" max="5" min="1" color="indigo"
                        show-ticks="always" step="0.25"></v-slider>
                </v-sheet>
                <v-sheet>
                    <v-btn @click="add(idx)">
                        +
                    </v-btn>
                </v-sheet>
                <v-sheet>
                    <v-btn @click="reduce(idx)">
                        -
                    </v-btn>
                </v-sheet>
            </div>
        </v-container>
    </v-card-text>
    <v-card-text class="pt-1">
        <v-btn block @click="submit()">提交预测</v-btn>
    </v-card-text>


</template>
<script setup>
import axios from '../../axios/index.js';
import { ref } from 'vue';
import _ from "lodash";
import { host } from "@/components/global.js";
import Schema from 'async-validator';
import Loader from "@/components/loader.vue";
const loader = ref()
const props = defineProps(['parentData'])
const data = props.parentData
const snackbarShow = ref({ is: false, msg: "" })

const tickLabels = {
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5'
}

function add(idx) {
    data.chart.splice(idx, 0, _.cloneDeep(data.chart[idx]))
    data.ship.splice(idx, 0, _.cloneDeep(data.ship[idx]))
    data.weight.splice(idx, 0, 0.250)
    data.indicatorItems.splice(idx, 0, data.indicatorItems[idx])
}

function reduce(idx) {
    if (data.chart.length > 1) {
        data.chart.splice(idx, 1)
        data.weight.splice(idx, 1)
        data.ship.splice(idx, 1)
        data.indicatorItems.splice(idx, 1)
    }
    else {
        snackbarShow.value.msg = '至少保留一个'
        snackbarShow.value.is = true
    }
}

const rules = {
    experts: { required: true, type: 'number', message: '请检查输入的人数是否是数字' },
}
const validator = new Schema(rules)

function submit() {
    validator.validate({ experts: data.numbers })
        .then(() => {
            loader.value.switchLoader()
            axios.post(
                host + 'mc_for_fce/', { idx_num: data.indicatorItems, experts_num: data.numbers }
            ).then(res => {
                for (let [idx, _] of res.data.entries()) {
                    data.chart[idx] = res.data[idx]
                }
                loader.value.switchLoader()
            }).catch(() => {
                loader.value.switchLoader()
                snackbarShow.value.msg = '发生错误，请联系开发者'
                snackbarShow.value.is = true
            })
        })
        .catch(({ errors }) => {
            snackbarShow.value.msg = errors[0].message
            snackbarShow.value.is = true
        })
}



</script>