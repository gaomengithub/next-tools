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
                    注意事项
                </v-card-title>
                
                <v-card-text>
                    1、word文档中必须包含“参考文献”，字之间不能有空格。<br>
                    2、标记的和未标记的使用颜色区分，未能标记的文献采用黄色。<br>
                    3、会返回两个版本，一个版本带有脚注，另外一个没有。
                    <v-divider></v-divider>
                    <v-file-input accept=".doc,.docx" label="需要标记的Word" hide-details="auto" show-size @change="wsUploadWord">
                    </v-file-input>
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
const loader = ref()
const show = ref({ is: false, msg: "" })
const status = ref('开始')
const timestamp = Date.now()



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
    const ws = new WebSocket(`ws://${wsHost}ws/citation-mark/upload_word/${timestamp}`)
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