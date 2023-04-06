<template>
    <Loader ref="loader"></Loader>
    <v-snackbar :timeout="3000" multi-line v-model="show.is" position="sticky">
        {{ show.msg }}
    </v-snackbar>
    <v-container>
        <v-card>
            <v-container>
                <v-card-title>
                    注意事项：
                </v-card-title>
                <v-card-subtitle>
                    1、复制粘贴需要整理的文献综述信息到输入框<br />
                    2、文献综述信息的获取请看相关教程。<br />
                    3、需要选择文献综述整理的格式。<br />
                </v-card-subtitle>
                <v-divider></v-divider>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-select v-model="isType" variant="underlined" density="comfortable" hide-details="auto"
                                :items="type" style="justify-content: center; width:150px" label="选择文献标注样式">
                            </v-select>
                            <v-spacer></v-spacer>
                            <v-btn @click="generate">生成文献综述</v-btn>
                            <v-spacer></v-spacer>
                            <v-btn @click="restContent">清除内容</v-btn>
                        </v-row>
                    </v-container>
                    <v-row>
                        <v-container>
                            <v-textarea v-model="content" background-color="light-blue" color="black" auto-grow
                                hide-details="auto">
                            </v-textarea>
                        </v-container>
                    </v-row>
                </v-card-text>
            </v-container>
        </v-card>
    </v-container>

</template>


<script setup >
import { ref } from 'vue';
import axios from "axios";
import Schema from 'async-validator';
import Loader from '@/components/Loader.vue';
import { host } from '@/components/global';

const type = ['人名+年份+摘要+外标注', '人名+年份+摘要+内标注', '人名+摘要+外标注', '人名+摘要+内标注','摘要+（人名+标注，年份）','人名+年份+标注+摘要','人名+标注+年份+摘要','人名+标注+摘要']
const content = ref("")
const isType = ref("")
const loader = ref()
const show = ref({ is: false, msg: "" })

function restContent() {
    content.value = ""
}

const rules = {
    type: { required: true, message: '请选择样式' },
    content: { required: true, message: '请输入内容' },
}
const validator = new Schema(rules)


function generate() {
    validator.validate({ type:isType.value, content: content.value })
        .then(() => {
            loader.value.switchLoader()
            axios.post(host + 'literature-review/', {
                'content': content.value,
                //'school': isSchool.value,
                'type': isType.value
            }, {
                responseType: 'blob',
                header: {
                    'Content-Type': 'application/json;charset=UTF-8',
                }
            }).then(res => {
                exportWord(res);
                loader.value.switchLoader()
            }).catch(() => {
                loader.value.switchLoader()
            })
        })
        .catch(({ errors }) => {
            show.value.is = true
            show.value.msg = errors[0].message
        })

}

function exportWord(res) {
    const blob = new Blob([res.data]);
    const fileName = res.headers['filename'] + '.docx';
    const elink = document.createElement('a');
    elink.download = fileName;
    elink.style.display = 'none';
    elink.href = URL.createObjectURL(blob);
    document.body.appendChild(elink);
    elink.click();
    URL.revokeObjectURL(elink.href); // 释放URL 对象
    document.body.removeChild(elink);
}

</script>