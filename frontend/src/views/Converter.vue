<template>
    <v-container>
        <v-card>
            <v-card-title>
                注意事项：
            </v-card-title>
            <v-card-subtitle>
                1、参考文献前不要加序号；<br />
                2、标点符号要用半角；<br />
                3、文献信息要全。
            </v-card-subtitle>
            <v-divider ></v-divider>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-radio-group v-model="radioGroup" inline hide-details="auto">
                            <v-radio value="APA-GB" label="APA转GB-T7714-2005" density="compact"></v-radio>
                            &nbsp;
                            <v-radio value="GB-APA" label="GB-T7714-2005转APA" density="compact"></v-radio>
                        </v-radio-group>
                        <v-btn>一键转换</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn>一键复制</v-btn>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-text style="padding-top: 0;">
                <v-textarea background-color="light-blue" color="black" label="点击参考文献" auto-grow="ture"
                    hide-details="auto">
                </v-textarea>
            </v-card-text>
        </v-card>
    </v-container>


</template>
<script setup >
import { ref } from 'vue';

const radioGroup = ref("GB-APA")

</script>