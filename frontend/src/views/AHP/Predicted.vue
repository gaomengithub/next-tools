<template>
    <Loader ref="loader"></Loader>
    <v-snackbar :timeout="3000" multi-line v-model="snackbarShow.is">
        {{ snackbarShow.msg }}
    </v-snackbar>
    <v-container>
        <v-card>
            <v-container>
                <v-card-title class="d-flex align-center justify-space-between flex-row">
                    <v-sheet>预测条件</v-sheet>
                    <v-sheet>
                        <v-switch v-model="inputModes" hide-details="auto" color="info" true-value="true"
                            false-value="false" label="转入输入模式">
                        </v-switch>
                    </v-sheet>
                </v-card-title>
                <v-card-text>
                    <v-card-title v-for="(_, idx) in items" v-if="inputModes == 'false'"
                        class="d-flex align-center justify-space-between flex-row py-1">
                        <v-sheet class="w-75">
                            <v-select v-model="items[idx]" :items="options" item-title="state" item-value="abbr"
                                variant="outlined" density="compact" hide-details="auto"
                                :prepend-icon="`mdi-numeric-` + (idx + 1)" single-line >
                            </v-select>
                        </v-sheet>
                        <v-sheet>
                            <v-btn @click="add(idx)"> + </v-btn>
                        </v-sheet>
                        <v-sheet>
                            <v-btn @click="reduce(idx)"> - </v-btn>
                        </v-sheet>
                    </v-card-title>
                    <v-card-title v-for="(_, idx) in items" v-if="inputModes == 'true'"
                        class="d-flex align-center justify-space-between flex-row py-1">
                        <v-sheet class="w-75">
                            <v-text-field color="primary" hide-details="auto" v-model="items[idx]" variant="solo"
                                single-line density="compact" placeholder="不控制" :prepend-icon="`mdi-numeric-` + (idx + 1)">
                            </v-text-field>
                        </v-sheet>
                        <v-sheet>
                            <v-btn @click="add(idx)"> + </v-btn>
                        </v-sheet>
                        <v-sheet>
                            <v-btn @click="reduce(idx)"> - </v-btn>
                        </v-sheet>
                    </v-card-title>
                </v-card-text>
                <v-card-text class="d-flex align-center justify-space-between flex-row py-1">
                    <v-sheet :style="{ color: residualWeight < 0 ? 'red' : 'black' }">剩余权重：{{ residualWeight.toFixed(4)
                    }}</v-sheet>
                    <v-sheet>
                        <v-btn @click="rest"> 重置 </v-btn>
                    </v-sheet>
                    <v-sheet>
                        <v-btn @click="submit"> 提交 </v-btn>
                    </v-sheet>
                </v-card-text>
            </v-container>
        </v-card>
    </v-container>
</template>

<script setup >
import axios from '../../axios/index.js';
import { ref, watch, computed } from 'vue';
import { host } from "../../components/global.js";
import Schema from 'async-validator';
import _ from "lodash";
import Loader from "@/components/loader.vue";
const loader = ref()
const snackbarShow = ref({ is: false, msg: "" })
const inputModes = ref('false')
const items = ref(["", "", "", ""])
const props = defineProps(['parentData'])
const data = props.parentData
const options = ref([
    { state: "较平均值低(-80%)，", abbr: "" },
    { state: "较平均值低(-60%)，", abbr: "" },
    { state: "较平均值低(-40%)，", abbr: "" },
    { state: "较平均值低(-25%)，", abbr: "" },
    { state: "较平均值高(+35%)，", abbr: "" },
    { state: "较平均值高(+55%)，", abbr: "" },
    { state: "较平均值高(+85%)，", abbr: "" },
    { state: "较平均值高(+100%)，", abbr: "" },
    { state: "较平均值高(+120%)，", abbr: "" },
])
const avgWeight = computed(() =>
    1 / items.value.length
)
const residualWeight = computed(() =>
    1 - eval(items.value.map(item => Number(item)).join('+'))
)
// 实时修改下拉选项
watch(items.value, () => {
    for (let [idx, _option] of options.value.entries()) {
        options.value[idx].state = _option.state.match(/较平均值高\(\+\d+%\)，|较平均值低\(-\d+%\)，/) + ((_option.state.match(/\+\d+|-\d+/) / 100 + 1) * avgWeight.value).toFixed(4)
        options.value[idx].abbr = ((_option.state.match(/\+\d+|-\d+/) / 100 + 1) * avgWeight.value).toFixed(4)
    }
}, {
    immediate: true
})

function rest() {
    items.value = ["", "", "", ""]
}

const rules = {
    residualWeight: { required: true, type: 'number', min: -2, max: 2, message: '请检查输入的是否是数字，权重是否合理' },
}
const validator = new Schema(rules)

function submit() {
    validator.validate({ residualWeight: residualWeight.value })
        .then(() => {
            loader.value.switchLoader()
            const _data = _.cloneDeep(items.value).map(item => item == "" ? '不控制' : item)
            axios.post(host + 'ga_for_ahp/', _data
            ).then(res => {
                // 修改判断矩阵和参数
                data.calculation.judge = res.data
                loader.value.switchLoader()
            }).catch(() => {
                snackbarShow.value.msg = '出现未知错误，请联系开发者。'
                snackbarShow.value.is = true
                loader.value.switchLoader()
            })
        })
        .catch(({ errors }) => {
            snackbarShow.value.is = true
            snackbarShow.value.msg = errors[0].message
        })
}
function add(idx) {
    if (items.value.length < 9) {
        items.value.splice(idx + 1, 0, "")
    }
    else{
        snackbarShow.value.is = true
        snackbarShow.value.msg = '维度不能超过9。'

    }
}
function reduce(idx) {
    if (items.value.length > 2) {
        items.value.splice(idx, 1)
    }
    else{
        snackbarShow.value.is = true
        snackbarShow.value.msg = '维度不能低于2。'
    }
}

</script>
<style scoped>
:deep(.v-field--single-line input) {
    transition: none;
    padding-top: 0;
    padding-bottom: 0;
}
</style>