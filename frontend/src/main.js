import { createApp } from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";


// import * as Sentry from "@sentry/vue";
// import { BrowserTracing } from "@sentry/tracing";


// import { loadFonts } from "./plugins/webfontloader";
//import { createPinia } from "pinia";
import VueLatex from 'vatex'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import vue3videoPlay from "vue3-video-play";
import "vue3-video-play/dist/style.css";
// import '@mdi/font/css/materialdesignicons.css';
//const pinia = createPinia();
// import JsonViewer from "vue3-json-viewer";
// if you used v1.0.5 or latster ,you should add import "vue3-json-viewer/dist/index.css"
// import "vue3-json-viewer/dist/index.css";
// import { createPinia } from 'pinia'
// import piniaPluginPersist from 'pinia-plugin-persist'

// const store = createPinia()
// store.use(piniaPluginPersist)




const app = createApp(App);

// Sentry.init({
//     app,
//     dsn: "https://a9ba7a53fb594c65ac5e077f7460420b@sentry.infinite-primes.com/8",
//     integrations: [
//       new BrowserTracing({
//         routingInstrumentation: Sentry.vueRouterInstrumentation(router),
//         tracingOrigins: ["localhost", "my-site-url.com", /^\//],
//       }),
//     ],
//     // Set tracesSampleRate to 1.0 to capture 100%
//     // of transactions for performance monitoring.
//     // We recommend adjusting this value in production
//     tracesSampleRate: 1.0,
//   });

app.use(vue3videoPlay);
app.use(router);
app.use(vuetify);
app.use(VueLatex);
// app.use(store);
// app.use(JsonViewer);


// app.use(pinia);

app.mount("#app");
