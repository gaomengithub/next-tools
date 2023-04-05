
import axios from "axios";
import router from "@/router/index";
axios.interceptors.request.use(function (config) {
    const token = localStorage.getItem('token') //本地环境的token
    config.headers = {
        Authorization: 'Bearer ' + token,
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});

axios.interceptors.response.use(
    function (response) {
        // 对响应数据做点什么
        return response;
    },
    function (error) {
        if (error.response.status == 401) {
            router.push({
                path: '/tools-next/login'
            });
            return Promise.reject(error);
        } else {
            return Promise.reject(error);
        }
    });

export default axios;

