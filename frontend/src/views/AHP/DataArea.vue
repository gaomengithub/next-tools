<template>
  <v-snackbar :timeout="4000" multi-line v-model="snackbarShow.is">
    {{ snackbarShow.msg }}
  </v-snackbar>
  <v-container>
    <v-row>
      <v-col cols="6" class="d-flex align-center">
        <v-card v-if="data.goal.judge.length != 0" class="mb-1 mt-1">
          <v-card-text>
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col" style="width: 7%;">
                    {{ data.goal.prefix }}
                  </th>
                  <th scope="col" v-for="idx in data.goal.judge.length">{{ data.goal.prefix + idx }}</th>
                  <th scope="col" v-if="data.display == 'true'" v-for="item in ['行积', '方根']">{{ item }}</th>
                  <th scope="col">权重</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in data.goal.judge">
                  <th scope="row">{{ data.goal.prefix + (idx + 1) }}</th>
                  <!-- 生成判断矩阵 -->
                  <td v-for="(_item, _idx) in item" :style="{ width: 65 / data.goal.judge.length + '%' }">
                    {{ _item }}
                  </td>
                  <!-- 行积和方根 -->
                  <td v-if="data.display == 'true'" v-for="item in data.goal.productRowAndThRoot[idx]">{{ item }}</td>
                  <!-- 权重 -->
                  <td>{{ data.goal.weight[idx] }}</td>
                </tr>
              </tbody>
            </table>
            注：判断矩阵的λ<sub>max</sub>={{ data.goal.params.lamudaMax }}，RI={{ data.goal.params.RI }}，CI={{
                data.goal.params.CI
            }}， CR={{ data.goal.params.CR }}。
          </v-card-text>
          <v-card-actions>
            <v-btn @click="data.goal.judge = []" color="red"> 删除 </v-btn>
            <v-spacer></v-spacer>
            <v-btn :icon="equationShow ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="equationShow = !equationShow">
            </v-btn>
          </v-card-actions>
          <EquationLatex :parentData="data.goal" v-if="equationShow.goal"></EquationLatex>
        </v-card>
      </v-col>
      <!-- 准则层 -->
      <v-col cols="6">
        <v-card v-if="data.criterion.length != 0" v-for="(items, idxs) in data.criterion" class="mb-1 mt-1">
          <v-card-text>
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col" style="width: 7%;">
                    {{ items.prefix }}
                  </th>
                  <th scope="col" v-for="idx in items.judge.length">{{ items.prefix + idx }}</th>
                  <th scope="col" v-if="data.display == 'true'" v-for="item in ['行积', '方根']">{{ item }}</th>
                  <th scope="col">权重</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in items.judge">
                  <th scope="row">{{ items.prefix + (idx + 1) }}</th>
                  <!-- 生成判断矩阵 -->
                  <td v-for="(_item, _idx) in item" :style="{ width: 65 / items.judge.length + '%' }">
                    {{ _item }}
                  </td>
                  <!-- 行积和方根 -->
                  <td v-if="data.display == 'true'" v-for="item in items.productRowAndThRoot[idx]">{{ item }}</td>
                  <!-- 权重 -->
                  <td>{{ items.weight[idx] }}</td>
                </tr>
              </tbody>
            </table>
            注：判断矩阵的λ<sub>max</sub>={{ items.params.lamudaMax }}，RI={{ items.params.RI }}，CI={{
                items.params.CI
            }}， CR={{ items.params.CR }}。
          </v-card-text>
          <v-card-actions>
            <v-btn @click="data.criterion.splice(idxs, 1)" color="red" > 删除 </v-btn>
            <v-spacer></v-spacer>
            <v-btn @click="up(data.criterion, idxs)" :disabled="idxs == 0"> 上移 </v-btn>
            <v-spacer></v-spacer>
            <v-btn @click="down(data.criterion, idxs)" :disabled="idxs == data.criterion.length - 1"> 下移 </v-btn>
            <v-btn :icon="equationShow.criterion[idxs] ? 'mdi-chevron-up' : 'mdi-chevron-down'"
              @click="equationShow.criterion[idxs] = !equationShow.criterion[idxs]">
            </v-btn>
          </v-card-actions>
          <EquationLatex :parentData="data.criterion[idxs]" v-if="equationShow.criterion[idxs]"></EquationLatex>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <!-- 综合权重的表格 -->
  <v-container>
    <v-card v-if="data.goal.judge.length == data.criterion.length && data.criterion.length != 0">
      <v-container>
        <v-card-title>
          综合权重结果
        </v-card-title>
        <v-card-text>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th scope="col" v-for="item in ['二级指标权重', '三级指标权重', '综合权重']">{{ item }}</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(item, idx) in data.criterion">
                <tr>
                  <th :rowspan="item.weight.length">{{ data.goal.weight[idx] }}</th>
                  <td>{{ item.weight[0] }}</td>
                  <td>{{ (item.weight[0] * data.goal.weight[idx]).toFixed(3) }}</td>
                </tr>
                <tr v-for="_item in item.weight.slice(1)">
                  <td>{{ _item }}</td>
                  <td>{{ (_item * data.goal.weight[idx]).toFixed(3) }}</td>
                </tr>
              </template>
            </tbody>
          </table>
          建议从下往上选取，以正确复制表格。
        </v-card-text>
      </v-container>
    </v-card>
  </v-container>
</template>

<script setup >
import { ref, watch } from 'vue';
import EquationLatex from './EquationLatex.vue';
const props = defineProps(['parentData'])
const data = props.parentData
const equationShow = ref({ goal: false, criterion: [] })
const snackbarShow = ref({ is: false, msg: "" })

watch(data.criterion, () => {
  if (data.goal.judge.length == data.criterion.length && data.criterion.length != 0) {
    snackbarShow.value.is = true
    snackbarShow.value.msg = '已经生成综合权重结果，请下拉到底部。'
  }
})

//上下移动
function up(fieldData, index) {
  if (index != 0) {
    fieldData[index] = fieldData.splice(index - 1, 1, fieldData[index])[0];
  } else {
    snackbarShow.value.msg = '已经到顶了。'
    snackbarShow.value.is = true
  }
}
function down(fieldData, index) {
  if (index != fieldData.length - 1) {
    fieldData[index] = fieldData.splice(index + 1, 1, fieldData[index])[0];
  } else {
    snackbarShow.value.msg = '已经到底了。'
    snackbarShow.value.is = true
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
</style>