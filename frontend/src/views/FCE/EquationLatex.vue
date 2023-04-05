<template>
    <v-expand-transition>
        <div>
            <v-card-text>
                <vue-latex :expression=shipExpression display-mode :fontsize="10" />
                <vue-latex :expression=weightExpression display-mode :fontsize="10" />
                <vue-latex :expression=matxExpression display-mode :fontsize="10" />
            </v-card-text>
        </div>
    </v-expand-transition>
</template>
<script setup>
import { watch, ref, watchEffect } from 'vue';
const props = defineProps(['parentData'])
const data = props.parentData
const shipExpression = ref("")
const weightExpression = ref("")
const matxExpression = ref("")

watchEffect(() => {
    const header = "R=\\left[\\begin{array}{lllll}"
    let body = ""
    for (let item of data.ship) {
        body += item.join(" & ") + " \\\\"
    }
    shipExpression.value = header + body + "\\end{array}\\right]"
}
)

watch(data.weight, () => {
    const header = `"W=\\left[\\begin{array}{${data.weight.map(() => "l").join("")}}"`
    let body = ""
    body += data.weight.join(" & ")
    weightExpression.value = header.replaceAll("\"", "") + body + "\\end{array}\\right]"
}, {
    immediate: true
}
)

watchEffect(() => {
    const header = `"\\left[\\begin{array}{${data.matx.map(() => "l").join("")}}"`
    let body = ""
    body += data.matx.join(" & ")
    matxExpression.value = weightExpression.value.replace("W=", "") + shipExpression.value.replace("R=", "") + "=" + header.replaceAll("\"", "") + body + "\\end{array}\\right]"
})


</script>
