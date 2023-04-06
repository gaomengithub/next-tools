<template>
    <LoaderVue ref="switchLoader">
        正在进行：{{ status }}
    </LoaderVue>
    <v-snackbar :timeout="3000" multi-line v-model="show.is">
        {{ show.msg }}
    </v-snackbar>
    <v-container>
                <v-card>
                    <v-container>
                        <v-card-title>
                            第一步：选择学校。
                        </v-card-title>
                        <v-card-text>
                            <v-autocomplete density="compact" variant="outlined" :items="items" v-model="params.school">
                            </v-autocomplete>
                            <!-- <v-select v-model="params.school" :items="items" variant="outlined" density="compact"
                                hide-details="auto" > -->
                            <!-- </v-select> -->
                        </v-card-text>
                        <v-card-title>
                            第二步：选择辅助方式。
                        </v-card-title>
                        <v-card-text>
                            <v-checkbox label="样式辅助" hide-details="auto" v-model="assistBox.style">
                            </v-checkbox>
                            <v-card color="surface-variant" variant="tonal" v-show="assistBox.style">
                                <v-card-text class="pb-0">
                                    请选择样式的具体辅助方式：
                                    <v-radio-group hide-details="auto" v-model="assistKind">

                                        <v-radio label="默认样式，推断段落样式" value="0" disabled></v-radio>
                                        <v-radio label="默认样式，不推断段落样式" value="1"></v-radio>
                                        <v-radio label="新建样式，推断段落样式" value="2" disabled></v-radio>
                                        <v-radio label="新建样式，不推断段落样式" value="3" disabled></v-radio>
                                    </v-radio-group>
                                </v-card-text>
                                <v-card-text class="text-medium-emphasis text-caption pt-0">
                                    1、默认样式：[标题，标题 1，标题 2，标题 3，正文，题注，TOC 1，TOC 2，TOC 3，页眉，页脚]。<br>
                                    2、新建样式:[_标题，_标题 1，_标题 2，_标题 3，_正文，_题注，_TOC 1，_TOC 2，_TOC 3，_页眉，_页脚]
                                </v-card-text>
                            </v-card>
                            <v-checkbox label="页面设置辅助" hide-details="auto" v-model="assistBox.page" disabled>
                            </v-checkbox>
                            <v-checkbox label="页眉页脚内容辅助" hide-details="auto" v-model="assistBox.headers" disabled>
                            </v-checkbox>
                            <v-checkbox label="表格样式辅助" hide-details="auto" v-model="assistBox.table" disabled>
                            </v-checkbox>

                        </v-card-text>
                        <v-card-title>
                            第三步：上传文件，等待完成。
                        </v-card-title>
                        <v-card-text>
                            <v-file-input accept=".doc,.docx" label="需要排版的文档" hide-details="auto" style="height: 60px;"
                                @change="wsTypeset">
                            </v-file-input>
                        </v-card-text>
                    </v-container>
                </v-card>
            <!-- <v-col cols="6">
                <v-card>
                    <v-container>
                        <v-card-title>
                            目标学校样式信息
                        </v-card-title>
                        <v-card-text>
                            <v-card color="surface-variant" variant="tonal"> -->
            <!-- <v-card-text class="text-medium-emphasis text-caption"> -->
            <!-- <JsonViewer :value="schoolConfig" theme="jv-light" /> -->
            <!-- {{ schoolConfig }} -->
            <!-- </v-card-text> -->
            <!-- </v-card>
                        </v-card-text>
                    </v-container>
                </v-card>
            </v-col> -->

    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import LoaderVue from '@/components/loader.vue';
import axios from 'axios';
import { host, wsHost } from '@/components/global.js';
const items = ref([])
const params = ref({ school: "厦门大学", other: '', filename: '' })
const show = ref({ is: false, msg: "" })
const switchLoader = ref()
const assistBox = ref({ style: true, page: false, headers: false, table: false })
const assistKind = ref("1")
const status = ref("开始");
const timestamp = Date.now()



onMounted(() => {
    //get list of schools
    axios.get(host + 'get_schools_list')
        .then(res => {
            items.value = res.data
        })
        .catch(() => {
            show.value.is = true
            show.value.msg = "获取学校列表失败，请检查网络。"
        })
})


function wsTypeset(event) {
    switchLoader.value.switchLoader()
    const ws = new WebSocket(`ws://${wsHost}ws/typeset/${timestamp}`)
    ws.binaryType = 'arraybuffer'
    ws.onopen = function () {
        params.value.filename = event.target.files[0].name;
        ws.send(JSON.stringify(params.value));
        wsUploadFile(event, ws)
        console.log("websocket is connected")
    };

    ws.onmessage = function (evt) {
        status.value = '正在传输Word文档'
        try {
            const _json = JSON.parse(evt.data)
            if ('status' in _json) {
                status.value = _json.status;
            }
        } catch (err) {
            exportWord(evt);
            switchLoader.value.switchLoader()
        }
    };
    ws.onclose = function () {
        console.log("websocket is disconnected");
    };

}
function exportWord(res) {
    const blob = new Blob([res.data]);
    // console.log(res.headers['file_type'])
    // const fileName = res.headers['file_name'] + '\.' + res.headers['file_type'];
    const fileName = timestamp.toString() + params.value.filename

    const elink = document.createElement('a');
    elink.download = fileName;
    elink.style.display = 'none';
    elink.href = URL.createObjectURL(blob);
    document.body.appendChild(elink);
    elink.click();
    URL.revokeObjectURL(elink.href); // 释放URL 对象
    document.body.removeChild(elink);
}


function wsUploadFile(event, ws) {
    let file = event.target.files[0];
    // send params
    let reader = new FileReader();
    let rawData = new ArrayBuffer();
    reader.readAsArrayBuffer(file)
    // reader.error = function(){
    //     console.log('an error occurred during the upload error occurred')
    // }
    reader.onload = function (e) {
        rawData = e.target.result;
        ws.send(rawData);
        console.log('file upload is completed')
    };

}
</script>
