import { defineStore } from "pinia";

export const useActiveStore = defineStore({
    id: "active",
    state: () => ({
        active: '/',
        username:''
    }),
    getters: {

    },
    // 开启数据缓存 若 需要state 中的变量页面刷新数据缓存 需要调用 actions 中的方法
    actions: {
        setActive(active) {
            this.active = active
        },
        setUsername(username){
            this.username = username
        }
    },
    persist: {
        enabled: true, // 开启数据缓存
    }
});