<template>
    <v-container>
        <v-card>
            <v-container>
                <v-card-title>
                    操作说明教程
                </v-card-title>
                <v-card-text>
                    <videoVue :videoUrl="videoUrl" ></videoVue>
                </v-card-text>
                <v-card-title>
                    常见问题解答：
                </v-card-title>
                <v-card-text>
                    问题1：预测的结果如果不满意怎么办？
                    <br />
                    回答1：可以再次点击提交，如果结果仍不满意，可以在计算矩阵中手动调整。
                </v-card-text>
            </v-container>
        </v-card>
    </v-container>
</template>


<script setup>
import { host } from '@/components/global';
import videoVue from '@/components/video.vue';
const videoUrl = host + 'ahp_readme_video/'
</script>
