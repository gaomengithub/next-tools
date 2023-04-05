<template>
    <v-expand-transition>
        <div>
            <v-divider></v-divider>
            <v-card-text>
                举例说明计算过程：<br />
                第一步，计算每一行元素乘积：
                <vue-latex v-for="item in data.equation.proudct" :expression=item display-mode :fontsize="10" />
                第二步，计算每一行元素乘积的{{ data.equation.des }}次方根:
                <vue-latex v-for="item in data.equation.throot" :expression=item display-mode :fontsize="10" />
                第三步，对上述{{ data.equation.des }}个次方根求和：
                <vue-latex :expression=data.equation.throotSum display-mode :fontsize="10" />
                第四步，计算指标权重：
                <vue-latex v-for="item in data.equation.weight" :expression=item display-mode :fontsize="10" />
            </v-card-text>
        </div>
    </v-expand-transition>
</template>
<script setup>
const props = defineProps(['parentData'])
const data = props.parentData
</script>
