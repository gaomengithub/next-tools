<template>
    <v-dialog v-model="loader" :scrim="true" persistent>
        <div class="d-flex justify-center">
            <v-card color="primary" class="w-50">
                <v-card-text>
                    请耐心等待完成
                </v-card-text>
                <v-card-text>
                    <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                </v-card-text>
                <v-card-text class="mb-1">
                    <slot>
                    </slot>
                </v-card-text>
            </v-card>
        </div>

    </v-dialog>
</template>
<script setup >
import { ref } from 'vue';
const loader = ref(false)
function switchLoader() {
    loader.value = !loader.value
}

defineExpose({ switchLoader })
</script>