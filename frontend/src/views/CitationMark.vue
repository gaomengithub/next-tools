<template>
    <Loader ref="loader">
        正在进行：{{ status }}
    </Loader>
    <v-snackbar :timeout="3000" multi-line v-model="show.is">
        {{ show.msg }}
    </v-snackbar>
    <v-container>
        <v-card>
            <v-container>
                <v-card-title>
                    第一步：上传Word
                </v-card-title>
                <v-card-text>
                    <v-file-input accept=".doc,.docx" label="需要标记的Word" hide-details="auto" show-size @change="wsUploadReport">
                    </v-file-input>
                </v-card-text>
                <v-card-title>
                    第二步：选择返回的版本（可多选）
                </v-card-title>
                <v-card-text>
                    <v-chip-group v-model="params.is" column multiple>
                        <v-chip v-for="item in toggle" filter outlined label>
                            {{ item }}
                        </v-chip>
                    </v-chip-group>
                </v-card-text>
                <v-card-title>
                    第三步：点击开始按钮，等待完成。
                </v-card-title>
                <v-card-text>
                    <v-btn block >
                        开始
                    </v-btn>
                    <!-- <v-file-input accept=".doc,.docx" hide-details="auto" label="需要标注的文档" density="default" show-size
                        @change="wsUploadWord" :disabled="params.is.length == 0">
                    </v-file-input> -->
                </v-card-text>
            </v-container>
        </v-card>
    </v-container>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { host, wsHost } from '@/components/global.js'
import Loader from '@/components/loader.vue';
let params = ref({ is: [], colors: '', filename: '' })
const toggle = ref(["带有脚注的版本","不带脚注的版本"])
const loader = ref()
const show = ref({ is: false, msg: "" })
const status = ref('开始')
const timestamp = Date.now()

function wsUploadReport(event) {
    loader.value.switchLoader()
    const ws = new WebSocket(`ws://${wsHost}ws/mark_color/upload_report_extract_colors/${timestamp}`)
    ws.binaryType = 'arraybuffer'
    ws.onopen = function () {
        wsUploadFile(event, ws)
    };
    ws.onmessage = function (evt) {
        const _json = JSON.parse(evt.data);
        status.value = _json.status
        if ("toggle" in _json) {
            toggle.value = _json.toggle.split("|");
            params.value.colors = _json.colors
            loader.value.switchLoader();
        }
    };
    // ws.onclose = function () {
    //     console.log("websocket is disconnected");
    // };
    ws.onerror = function () {
        loader.value.switchLoader()
        show.value.is = true
        show.value.msg = "websocket连接发生错误请联系开发者。"
    }
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
        // console.log('file upload is completed')
    };
}


function wsUploadWord(event) {
    loader.value.switchLoader()
    const ws = new WebSocket(`ws://${wsHost}ws/mark_color/upload_word_mark_color/${timestamp}`)
    ws.binaryType = 'arraybuffer'
    ws.onopen = function () {
        params.value.filename = event.target.files[0].name;
        ws.send(JSON.stringify(params.value));
        wsUploadFile(event, ws)
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
            loader.value.switchLoader()
        }
    };
    // ws.onclose = function () {
    //     console.log("websocket is disconnected");
    // };
    ws.onerror = function () {
        loader.value.switchLoader()
        show.value.is = true
        show.value.msg = "websocket连接发生错误请联系开发者。"
    }
}


// watchEffect(() => {
//     params.is = amenities.value
// })

function uploadReport(event) {

    let formData = new FormData()
    formData.append('file', event.target.files[0])
    loader.value.switchLoader()
    axios({
        url: host + "mark_color/check_report/",
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': "multipart/form-data",
        },
        // onUploadProgress: progressEvent => {
        //     processReport.value = (progressEvent.loaded / progressEvent.total * 100 | 0)
        // }
    }).then(res => {
        toggle.value = res.data.toggle
        params = res.data
        loader.value.switchLoader()
    })
}



// onMounted(() => {
//     // websocket

//     ws = new WebSocket(`ws://${wsHost}ws/mark_color/upload_pdf/${client_id}`)
//     // 连接建立后的回调函数
//     ws.binaryType = 'arraybuffer'
//     ws.onopen = function () {
//         console.log("已经建立websocket连接")
//     };

//     // 接收到服务器消息后的回调函数
//     ws.onmessage = function (evt) {
//         status.value = evt.data;
//         console.log(evt.data)
//     };
//     // 连接关闭后的回调函数
//     ws.onclose = function () {
//         // 关闭 websocket
//         console.log("连接已关闭...");
//     };
// })

// onBeforeUnmount(() => {
//     ws.close()
//     ws = null
// })



function uploadWord(event) {
    let formData = new FormData()
    formData.append('file', event.target.files[0])
    formData.append('params', JSON.stringify(params)) // params need change
    formData.append('client_id', client_id.toString())
    loader.value.switchLoader()

    axios({
        url: host + "mark_color/mark_word/",
        method: 'post',
        data: formData,
        responseType: 'blob',
        headers: {
            'Content-Type': "multipart/form-data",
        },
        onUploadProgress: progressEvent => {
            processReport.value = (progressEvent.loaded / progressEvent.total * 100 | 0)
        }
    }).then(res => {
        exportWord(res);
        loader.value.switchLoader()
        amenities.value = []

    }).catch(() => {
        console.log('后台报错了')
    })
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


</script>
<style scoped="scoped">
:deep(.v-field__field) {
    height: 50px;
}
</style>