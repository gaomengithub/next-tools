<template>
  <div class="py-4">
    <v-img class="mx-auto mb-10" max-width="64" src="https://portal.infinite-primes.com/favicon.ico"></v-img>
    <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>
      <v-text-field v-model="username" density="compact" placeholder="输入手机号" prepend-inner-icon="mdi-cellphone"
        variant="outlined">
      </v-text-field>
      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Password
      </div>
      <v-text-field v-model="password" :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'" density="compact" placeholder="输入密码" prepend-inner-icon="mdi-lock-outline"
        variant="outlined" @click:append-inner="visible = !visible"></v-text-field>
      <v-card v-if="loginErr.show" class="mb-6" color="surface-variant" variant="tonal">
        <v-card-text class="text-medium-emphasis text-caption">
          {{ loginErr.info }}
        </v-card-text>
      </v-card>
      <v-btn @click="login" block class="mb-8" color="blue" size="large" variant="tonal">
        登录
      </v-btn>
      <v-progress-linear :active="loading" :indeterminate="loading" absolute bottom></v-progress-linear>
    </v-card>
  </div>
</template>
<script setup>
import { host } from '@/components/global.js'
import axios from 'axios';
import router from '@/router';
import { ref, onMounted } from 'vue'
// import { useActiveStore } from '/src/store/index.js'
const visible = ref(false)
const loading = ref(false)
const loginErr = ref({ show: false, info: '' })
const username = ref("")
const password = ref("")
// const store = useActiveStore()
function login() {
  loading.value = true;
  axios.post(host + 'login_for_access_token/', { username: username.value, password: password.value })
    .then(function (response) {
      // console.log(response)
      localStorage.setItem("token", response.data.access_token);
      router.push("/tools-next/")
      // store.setUsername(response.data.username)
    }).catch(function (error) {
      loginErr.value.info = error.response.data.detail
      loginErr.value.show = true;
      loading.value = false
    })
}

onMounted(() => {
  // 按下回车键=点击登录那妞
  document.onkeydown = function (e) {
    e = window.event || e;
    if ((e.code === 'Enter') && (router.currentRoute.value.fullPath === '/tools-next/login' || router.currentRoute.value.fullPath === '/')) {
      login();
    }
  }
})
</script>

