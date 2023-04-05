<template>
  <v-tabs v-model="tab" centered grow color="primary">
    <v-tab value="calculate">计算</v-tab>
    <v-tab value="predicted">预测</v-tab>
    <v-tab value="readme">说明</v-tab>
  </v-tabs>
  <v-window v-model="tab">
    <v-window-item value="calculate">
      <Calculate :parentData="data" />
      <DataArea :parentData="data" />
    </v-window-item>
    <v-window-item value="predicted">
      <Predicted :parentData="data" />
      <Calculate :parentData="data" />
      <DataArea :parentData="data" />
    </v-window-item>
    <v-window-item value="readme">
      <Readme></Readme>
    </v-window-item>
  </v-window>
</template>
<script setup>
import Readme from '@/views/AHP/Readme.vue'
import Calculate from "@/views/AHP/Calculate.vue";
import DataArea from "@/views/AHP/DataArea.vue";
import Predicted from "@/views/AHP/Predicted.vue";
import { reactive, ref } from "vue"
const tab = ref("calculate")

const data = reactive({
  calculation: {
    judge: [
      ["1", "1", "1", "1"],
      ["1", "1", "1", "1"],
      ["1", "1", "1", "1"],
      ["1", "1", "1", "1"],
    ],
    productRowAndThRoot: [
      ["1", "1"],
      ["1", "1"],
      ["1", "1"],
      ["1", "1"]
    ],
    weight: ["1", "1", "1", "1"],
    params: { lamudaMax: '', RI: '', CI: '', CR: '' },
    equation: { product: [], throot: [], throotSum: '', weight: [], des: '' },
    prefix: "C",
  },
  goal: {
    judge: [],
    productRowAndThRoot: [],
    weight: [],
    params: { lamudaMax: '', RI: '', CI: '', CR: '' },
    equation: { product: [], throot: [], throotSum: '', weight: [], des: '' },
    prefix: "C",
  },
  criterion: [], // { matrix: [], params: { lamudaMax: '', RI: '', CI: '', CR: '' } }
  display: 'true'
})

</script>



