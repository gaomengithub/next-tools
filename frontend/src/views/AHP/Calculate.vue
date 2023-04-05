<template>
  <v-snackbar :timeout="3000" multi-line v-model="snackbarShow.is">
    {{ snackbarShow.msg }}
  </v-snackbar>
  <v-container>
    <v-card>
      <v-container>
        <v-card-title class="d-flex align-center justify-space-between flex-row">
          <v-sheet>计算矩阵</v-sheet>
          <v-sheet>
            <v-switch v-model="data.display" label="展示行积和方根列" hide-details="auto" color="info" true-value="true"
              false-value="false">
            </v-switch>
          </v-sheet>
        </v-card-title>
        <v-card-text>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col" style="width: 7%;">
                  <input v-model="data.calculation.prefix" type="text"
                    class="form-control border-0 font-weight-bold text-subtitle-2">
                </th>
                <th scope="col" v-for="idx in data.calculation.judge.length">{{ data.calculation.prefix + idx }}</th>
                <th scope="col" v-if="data.display == 'true'" v-for="item in ['行积', '方根']">{{ item }}</th>
                <th scope="col">权重</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in data.calculation.judge">
                <th scope="row">{{ data.calculation.prefix + (idx + 1) }}</th>
                <!-- 生成判断矩阵 -->
                <td v-for="(_item, _idx) in item" :style="{ width: 65 / data.calculation.judge.length + '%' }">
                  <input v-model="data.calculation.judge[idx][_idx]" type="text" :disabled="_idx >= idx ? true : false"
                    class="form-control border-0 ">
                </td>
                <!-- 行积和方根 -->
                <td v-if="data.display == 'true'" v-for="item in data.calculation.productRowAndThRoot[idx]">{{ item }}
                </td>
                <!-- 权重 -->
                <td>{{ data.calculation.weight[idx] }}</td>
              </tr>
            </tbody>
          </table>
          注：判断矩阵的λ<sub>max</sub>={{ data.calculation.params.lamudaMax }}，RI={{ data.calculation.params.RI }}，CI={{
              data.calculation.params.CI
          }}， CR={{ data.calculation.params.CR }}。
        </v-card-text>
        <v-card-actions>
          <v-btn @click="add"> 添加维度 </v-btn>
          <v-spacer />
          <v-btn @click="reduce"> 减少维度 </v-btn>
          <v-spacer />
          <v-btn @click="reset"> 重置数据 </v-btn>
          <v-spacer />
          <v-btn @click="toGoal"> 放入目标层({{data.goal.judge.length}}) </v-btn>
          <v-spacer />
          <v-btn @click="toCriterion"> 放入准则层({{ data.criterion.length }}) </v-btn>
          <v-spacer></v-spacer>
          <v-btn :icon="equationShow ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="equationShow = !equationShow">
          </v-btn>
        </v-card-actions>
        <EquationLatex :parentData="data.calculation" v-if="equationShow"></EquationLatex>
      </v-container>
    </v-card>
  </v-container>
</template>
<script setup >
import { multiply } from 'mathjs';
import { ref, watch ,watchEffect } from 'vue';
import EquationLatex from './EquationLatex.vue';
import _ from "lodash";
const snackbarShow = ref({ is: false, msg: "" })
const equationShow = ref(false)
const props = defineProps(['parentData'])
const data = props.parentData
const inverse = { "1": "1", "2": "1/2", "3": "1/3", "4": "1/4", "5": "1/5", "6": "1/6", "7": "1/7", "8": "1/8", "9": "1/9", "1/2": "2", "1/3": "3", "1/4": "4", "1/5": "5", "1/6": "6", "1/7": "7", "1/8": "8", "1/9": "9" }
const RI = [0, 0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54]

function checkNum(num) {
  return Object.keys(inverse).indexOf(num) > -1 ? true : false
}

watchEffect(() => {
  //长度
  data.calculation.equation.des = data.calculation.judge.length

  if (data.calculation.judge.flat(2).every(checkNum)) {
    for (let [idx, item] of data.calculation.judge.entries()) {
      for (let [_idx, _item] of item.entries()) {
        if (idx > _idx) {
          data.calculation.judge[_idx][idx] = inverse[_item]
        }
      }
    };
    //计算行积和方根
    const throotVec = []
    const equationProduct = []
    const equationThroot = []

    for (let [idx, item] of data.calculation.judge.entries()) {
      const product = eval(item.join("*"))
      const throot = Math.pow(product, 1 / data.calculation.judge.length)
      throotVec.push(throot)
      data.calculation.productRowAndThRoot[idx] = [product.toFixed(3),throot.toFixed(3)]

      // 形成计算过程

      equationProduct.push(("M_".concat(idx + 1) + "=" + item.join("\\ast") + "=" + product.toFixed(3)))
      data.calculation.equation.product = equationProduct

      equationThroot.push("\\sqrt[" + data.calculation.judge.length + "]{M_".concat(idx + 1) + "}=" + throot.toFixed(3))
      data.calculation.equation.throot = equationThroot
    };
    //计算权重
    const throotSum = eval(throotVec.join("+"))

    data.calculation.equation.throotSum = "\\overset" + data.calculation.judge.length + "{\\underset{i=1}{\\sum M_i}}=" + throotSum.toFixed(3)
    const weightVec = []
    const equationWeight = []
    for (let [idx, item] of throotVec.entries()) {
      const weight = item / throotSum
      weightVec.push(weight)
      data.calculation.weight[idx] = weight.toFixed(3)
      // 形成计算过程

      equationWeight.push("W_" + (idx + 1) + "=\\frac{M_" + (idx + 1) + "}{\\displaystyle\\overset" + data.calculation.judge.length + "{\\underset{i=1}{\\sum M_i}}}=" + weight.toFixed(3))
      data.calculation.equation.weight = equationWeight
    };
    //将矩阵内字符串转换为数字
    const matx = []
    for (let item of data.calculation.judge) {
      matx.push(item.map(x => eval(x)))
    };
    //计算一致性
    let mmultVec = multiply(matx, weightVec)
    for (let [idx, item] of mmultVec.entries()) {
      mmultVec[idx] = item / weightVec[idx] / weightVec.length
    }
    const lamudaMax = eval(mmultVec.join('+'))
    data.calculation.params.lamudaMax = lamudaMax.toFixed(4)
    const CI = (lamudaMax - weightVec.length) / (weightVec.length - 1)
    data.calculation.params.CI = CI.toFixed(4)
    data.calculation.params.RI = RI[weightVec.length]
    const CR = Number(CI / RI[weightVec.length])
    data.calculation.params.CR = CR.toFixed(4)
  }
  else {
    snackbarShow.value.msg = '请严格按照标准的1-9分度表输入正确的数字。'
    snackbarShow.value.is = true
  }
})


function add() {
  if (data.calculation.judge.length < 9) {
    for (let item of data.calculation.judge) {
      item.push("1")
    }
    data.calculation.judge.push(_.cloneDeep(data.calculation.judge.at(-1)))
    data.calculation.productRowAndThRoot.push(["1", "1"])
    data.calculation.weight.push("1")
  }
  else {
    snackbarShow.value.msg = '判断矩阵的维度不应大于9。'
    snackbarShow.value.is = true
  }
}

function reduce() {
  if (data.calculation.judge.length > 2) {
    for (let item of data.calculation.judge) {
      item.pop()
    }
    data.calculation.judge.pop()
    data.calculation.productRowAndThRoot.pop()
    data.calculation.weight.pop()
  }
  else {
    snackbarShow.value.msg = '判断矩阵的维度不应小于2。'
    snackbarShow.value.is = true
  }
}

function reset() {
  while (data.calculation.judge.length > 4) {
    data.calculation.judge.pop()
    data.calculation.productRowAndThRoot.pop()
    data.calculation.weight.pop()
  }
  while (data.calculation.judge.length < 4) {
    data.calculation.judge.push(_.cloneDeep(data.calculation.judge.at(-1)))
    data.calculation.productRowAndThRoot.push(["1", "1"])
    data.calculation.weight.push("1")
  }
  for (let idx of Object.keys(data.calculation.judge)) {
    data.calculation.judge[idx] = ["1", "1", "1", "1"]
  }
}

function toGoal() {
  data.goal = _.cloneDeep(data.calculation)
}

function toCriterion() {
  data.criterion.push(_.cloneDeep(data.calculation))
}


</script>
<style scoped>
.form-control:disabled {
  background-color: #e5e5e5;
  opacity: 1;
  color: dimgray;
}

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
