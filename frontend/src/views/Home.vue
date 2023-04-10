<template>
  <v-layout>
    <v-app-bar>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title> 欢迎使用 </v-app-bar-title>
      <v-menu location="start">
        <template v-slot:activator="{ props }">
          <v-btn icon="mdi-dots-vertical" v-bind="props"></v-btn>
        </template>
        <v-list>
          <v-list-item v-for="item in menuItems" :value="item" router-link :to="{ path: item.path }"
            :disabled="item.disable" active-color="#1976D2" density="comfortable">
            <v-list-item-title v-text="item.title">
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" density="compact">
      <v-list>
        <v-list-subheader>工具类</v-list-subheader>
        <v-list-item v-for="(item, i) in toolsItems" :key="i" :value="item" router-link :to="{ path: item.path }"
          rounded="xl" density="comfortable" active-color="#1976D2" :disabled="item.disable">
          <template v-slot:prepend>
            <v-icon :icon="item.icon"></v-icon>
          </template>
          <v-list-item-title v-text="item.text"></v-list-item-title>
        </v-list-item>
        <v-list-subheader>方法类</v-list-subheader>
        <v-list-item v-for="(item, i) in methodItems" :key="i" :value="item" router-link :to="{ path: item.path }"
          rounded="xl" density="comfortable" active-color="#1976D2" :disabled="item.disable">
          <template v-slot:prepend>
            <v-icon :icon="item.icon"></v-icon>
          </template>
          <v-list-item-title v-text="item.text"></v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref } from "vue"
let drawer = ref(true);

const menuItems = [{
  title: '与我相关', path: "/tools-next/me", disable: true
},
{ title: '重新登录', path: "/tools-next/login", disable: false }
]


const methodItems = [
  //{ text: "熵权法", icon: "mdi-alpha-e-circle", path: "/tools-next/ewm", disable: false },
  { text: "层次分析法", icon: "mdi-alpha-a-circle", path: "/tools-next/ahp", disable: false },
  { text: "模糊综合评价法", icon: "mdi-alpha-f-circle", path: "/tools-next/fce", disable: false },
  //{ text: "模糊综合评价法", icon: "mdi-alpha-f-circle", path: "/tools-next/fce", disable: false },
];
// const modelItems = [
//   { text: "随机森林模型", icon: "mdi-alpha-a-circle" },
//   { text: "因子分析模型", icon: "mdi-flag" },
//   { text: "数据包络分析模型", icon: "mdi-clock" },
// ];
const toolsItems = [
  { text: "网站合集", icon: "mdi-folder", path: "/tools-next/web-list", disable: false },
  { text: "英文目录", icon: "mdi-google-ads", path: "/tools-next/en-dir", disable: false },
  { text: "查重标记", icon: "mdi-laser-pointer", path: "/tools-next/mark-color", disable: false },
  { text: "文献综述", icon: "mdi-file-find", path: "/tools-next/literature-review", disable: false },
  { text: "文献标记", icon: "mdi-target", path: "/tools-next/citation-mark", disable: false },
  { text: "排版辅助", icon: "mdi-layers-triple", path: "/tools-next/typeset", disable: false },
  { text: "格式转换", icon: "mdi-page-next", path: "/tools-next/converter", disable: true },
]
</script>
