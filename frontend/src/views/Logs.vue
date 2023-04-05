<template>
    <v-container>
        <v-card>
            <v-card-title>
                网站日志
            </v-card-title>
            <v-container>
                <v-timeline side="end">
                    <v-timeline-item v-for="item in items" dot-color="info" size="small">
                        <v-alert :value="true" color="info" icon="mdi-information" class="white--text">
                            {{ item.content }}
                        </v-alert>
                    </v-timeline-item>
                </v-timeline>
            </v-container>
        </v-card>
    </v-container>
</template>
<script setup>
import { ref } from 'vue'
const items = ref([
    {
        id: "2022.09.1",
        content: '2022.09.1版本目前试运行，使用过程中遇到任何问题，欢迎联系工具开发者。'
    },
    {
        id: "2022.09.1",
        content: '2022.09.1版本在第1版的基础上，优化了“网站合集”、“英文目录”、“查重标记”以及“文稿排版”工具的性能；同时新增“层次分析法”与“模糊综合评价法”两大数据处理工具'
    },

])  
</script>