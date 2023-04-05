<template>
    <v-snackbar :timeout="3000" multi-line v-model="snackbarShow.is">
        {{ snackbarShow.msg }}
    </v-snackbar>
    <slot>
    </slot>
    <v-card-text class="pb-1">
        <!-- 输入部分 -->
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th scope="col" style="width: 8%;">
                        <input type="text" v-model="data.perfix" class="form-control border-0 font-weight-bold ">
                    </th>
                    <th scope="col">V<sub>1</sub></th>
                    <th scope="col">V<sub>2</sub></th>
                    <th scope="col">V<sub>3</sub></th>
                    <th scope="col">V<sub>4</sub></th>
                    <th scope="col">V<sub>5</sub></th>
                    <th scope="col" style="width: 8%;">和</th>
                    <th scope="col" style="width: 8%;">差</th>
                    <th scope="col" colspan="3">
                        <input v-model.number="data.numbers" placeholder="在此输入人数"
                            class="form-control border-0 font-weight-bold ">
                    </th>
                </tr>
            </thead>
            <tbody>
                <template v-for="(item, idx) in data.chart" :key="idx">
                    <tr>
                        <th scope="row">{{ data.perfix + (idx + 1) }}</th>
                        <td v-for="(_item, _idx) in item" :key="_idx">
                            <input v-model="data.chart[idx][_idx]" class="form-control border-0 ">
                        </td>
                        <td> {{ data.chartSum[idx] }} </td>
                        <td :style="{ color: (data.diff[idx] == 0 ? 'black' : 'red') }">
                            {{ data.diff[idx] }}
                        </td>
                        <td>
                            <v-btn @click="match(idx)"> 自动配平 </v-btn>
                        </td>
                        <td>
                            <v-btn @click="add(idx)"> + </v-btn>
                        </td>
                        <td>
                            <v-btn @click="reduce(idx)"> - </v-btn>
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
    </v-card-text>
    <v-card-text class="d-flex justify-space-between pt-1 pb-1">
        <!-- 评价结果表格 -->
        <v-sheet class="w-50 mr-1">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col" style="width: 8%;"> {{ data.perfix }} </th>
                        <th scope="col">V<sub>1</sub></th>
                        <th scope="col">V<sub>2</sub></th>
                        <th scope="col">V<sub>3</sub></th>
                        <th scope="col">V<sub>4</sub></th>
                        <th scope="col">V<sub>5</sub></th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(item, idx) in data.chart" :key="idx">
                        <tr>
                            <th scope="row">{{ data.perfix + (idx + 1) }}</th>
                            <td v-for="(_item, _idx) in item" :key="_idx"
                                :style="{ color: (data.diff[idx] == 0 ? 'black' : 'red') }">
                                {{ _item }}
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </v-sheet>
        <!-- 隶属度表格 -->
        <v-sheet class="w-50 ml-1">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col" style="width: 8%;"> {{ data.perfix }} </th>
                        <th scope="col">V<sub>1</sub></th>
                        <th scope="col">V<sub>2</sub></th>
                        <th scope="col">V<sub>3</sub></th>
                        <th scope="col">V<sub>4</sub></th>
                        <th scope="col">V<sub>5</sub></th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(item, idx) in data.ship" :key="idx">
                        <tr>
                            <th scope="row">{{ data.perfix + (idx + 1) }}</th>
                            <td v-for="(_item, _idx) in item" :key="_idx"
                                :style="{ color: (data.diff[idx] == 0 ? 'black' : 'red') }">
                                {{ _item }}
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </v-sheet>
    </v-card-text>
    <v-card-text class="pt-1 pb-1">
        <!-- 权重 输入-->
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th scope="col" v-for="(_, idx) in data.weight">W<sub>{{ idx + 1 }}</sub></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td v-for="(_, idx) in data.weight" :key="idx">
                        <input v-model="data.weight[idx]" class="form-control border-0 ">
                    </td>
                </tr>
                <tr>
                    <td v-for="(item, idx) in data.weight" :key="idx">
                        {{ item }}
                    </td>
                </tr>
            </tbody>
        </table>

    </v-card-text>
    <v-card-text class="pt-1 pb-1">
        <!-- 权重 复制-->
        <table class="table table-bordered">
            <tbody>
                <tr>
                    <th>乘积</th>
                    <td v-for="(item, idx) in data.matx" :key="idx">
                        {{ item }}
                    </td>
                </tr>
            </tbody>
        </table>

    </v-card-text>
    <v-card-text class="pt-1 pb-1">
        <!-- 公式 -->
        <EquationLatex :parentData="data" />
    </v-card-text>
</template>

<script setup >
import { ref, watch ,watchEffect } from 'vue';
import _ from "lodash";
import { multiply } from 'mathjs';
import EquationLatex from '../FCE/EquationLatex.vue';
const props = defineProps(['parentData'])
const data = props.parentData

const snackbarShow = ref({ is: false, msg: "" })
// 修改和,差
watch([data.chart, () => data.numbers], () => {
    data.chartSum = data.chart.map(x => eval(x.join("+")))
    data.diff = data.chartSum.map(x => data.numbers - x)
}, {
    immediate: true,
})
watch(data.chart, () => {
    data.ship = data.chart.map(x => x.map(x => (x / data.numbers).toFixed(3)))
}, {
    immediate: true
})

watchEffect(() => {
    let matx = multiply(data.weight, data.ship)
    data.matx = matx.map(x => x.toFixed(3))
})


function match(idx) {
    for (let [_idx, _] of data.chart[idx].entries()) {
        while (eval(data.chart[idx].join("+")) < data.numbers) {
            const randIdx = parseInt(Math.random() * (5))
            data.chart[idx][randIdx] += 1
        }
        while (eval(data.chart[idx].join("+")) > eval(data.numbers)) {
            const randIdx = parseInt(Math.random() * (5))
            data.chart[idx][randIdx] = (data.chart[idx][randIdx] > 0) ? data.chart[idx][randIdx] - 1 : 0
        }
    }
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
function reset() {
    for (let idx of Object.keys(data.chart)) {
        data.chart[idx] = [1, 1, 1, 1, 1]
    }
}

</script>
<style scoped>
:deep(td) {
    vertical-align: middle;
    text-align: center;
    font-size: small;
}

:deep(th) {
    vertical-align: middle;
    text-align: center;
    font-size: small;
}

:deep(input) {
    vertical-align: middle;
    text-align: center;
    font-size: small;
}

.table {
    background-color: #e5e5e5;
    border-color: #bdbbbb;
}
</style>