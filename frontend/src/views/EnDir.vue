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
                    1、复制中文目录后直接粘贴即可。<br />
                    2、需要选择学校和目录序号序列。<br />
                </v-card-subtitle>
                <v-divider></v-divider>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-select v-model="isSchool" variant="underlined" density="comfortable" hide-details="auto"
                                :items="school" style="justify-content: center; width:70px" label="选择学校">
                            </v-select>
                            <v-spacer></v-spacer>
                            <v-select v-model="isType" variant="underlined" density="comfortable" hide-details="auto"
                                :items="type" style="justify-content: center; width:70px" label="选择目录序号序列">
                            </v-select>
                            <v-spacer></v-spacer>
                            <v-btn @click="generate">生成目录</v-btn>
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

const school = ['厦门大学', '西安交通大学', '山东大学', '山东科技大学', '广东工业大学', '河南理工大学']
const type = ['1/1.1/1.1.1', '第1章/1.1/1.1.1', '第一章/1.1/1.1.1', '第一章/第一节/一、']
const content = ref("")
const isSchool = ref("")
const isType = ref("")
const loader = ref()
const show = ref({ is: false, msg: "" })

function restContent() {
    content.value = ""
}

const rules = {
    isSchool: { required: true, message: '请选择学校。' },
    istype: { required: true, message: '请选择目录序列' },
    content: { required: true, message: '请输入目录内容' },
}
const validator = new Schema(rules)


function generate() {
    validator.validate({ isSchool: isSchool.value, istype: isType.value, content: content.value })
        .then(() => {
            loader.value.switchLoader()
            axios.post(host + 'dir_to_en/', {
                'content': content.value,
                'school': isSchool.value,
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