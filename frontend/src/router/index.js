import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue"
import AHPmain from "@/views/AHP/AHPmain.vue";
import WebList from "@/views/WebList.vue";
import EnDir from "@/views/EnDir.vue";
import MarkColor from "@/views/MarkColor.vue";
import TypeSet from "@/views/TypeSet.vue";
import Converter from "@/views/Converter.vue"
import FCE from "@/views/FCE/FCEmain.vue"
import axios from "@/axios/index.js";
import EWM from "@/views/EWM/EWMmain.vue"
import LiteratureReview from "@/views/LiteratureReview.vue"
import { createRouter, createWebHistory } from 'vue-router'
import {host} from "@/components/global.js";
import favicon from "/favicon.ico"
import CitationMark from "@/views/CitationMark.vue"

const routes = [
  {
    path: "/tools-next/login",
    component: Login
  },
  {
    path: "/tools-next/",
    component: Home,
    children: [
      {
        path: "/tools-next/ahp",
        component: AHPmain,
      },
      {
        path: "/tools-next/web-list",
        component: WebList,
      },
      {
        path: "/tools-next/en-dir",
        component: EnDir,
      },
      {
        path: "/tools-next/mark-color",
        component: MarkColor,
      },
      {
        path: "/tools-next/typeset",
        component: TypeSet,
      },
      {
        path: "/tools-next/converter",
        component: Converter,
      },
      {
        path: "/tools-next/fce",
        component: FCE,
      },
      {
        path: "/tools-next/ewm",
        component: EWM,
      },
      {
        path: "/tools-next/literature-review",
        component: LiteratureReview,
      },
      {
        path: "/tools-next/citation-mark",
        component: CitationMark,
      },
      {
        path: "/favicon.ico",
        component: favicon,
      },
      {
        path: "/tools-next/",
        component: WebList,
      },
      {
        path: "/:pathMatch(.*)",
        component: WebList,
      },
    ],
  },

  //   { path: "/about", component: About },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.path == '/tools-next/' && from.path !='/tools-next/login') {    
    axios.get(host + 'check_token_exp_time/')
    .then(function(){
      next();
    })
      .catch(function (error) {
        if (error.response.status == 401) {
          next({ path: '/tools-next/login' })
        }
      })
  } else next()
})




export default router;
