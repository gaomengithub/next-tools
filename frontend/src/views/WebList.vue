<template>
    <v-container v-for="item in items">
        <v-card class="mx-auto">
            <v-card-title>
                {{ item.title }}
            </v-card-title>
            <v-card-text>
                <v-row>
                    <v-col cols="4" v-for="n in 3">
                        <v-list lines="three"
                            :items="item.childen.slice((n - 1) * Math.ceil(item.childen.length / 3), Math.ceil(item.childen.length / 3) * n)"
                            item-props>
                            <template v-slot:subtitle="{ subtitle }">
                                <div v-html="subtitle"></div>
                            </template>
                        </v-list>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-container>
</template>
<script setup>
const items = [
    {
        title: "学术网站", childen: [
            {
                prependAvatar: 'https://static.deepl.com/img/logo/DeepL_Logo_darkBlue_v2.svg',
                title: 'DeepL翻译器',
                href: "https://www.deepl.com/translator",
                target: "_blank",
                subtitle: `<span>当需要更好的英文摘要时，可以试一试这个翻译器。</span>`,
            },
            {
                prependAvatar: 'QX.ico',
                title: '求学图书馆',
                href: "http://www.caj11.com/",
                target: "_blank",
                subtitle: `<span>公司已有账号，可在群公告获取账户信息。</span>`,
            },
            {
                prependAvatar: '90.png',
                title: '90图书馆',
                href: "http://www.90tsg.com/",
                target: "_blank",
                subtitle: `<span>公司已有账号，可在群公告获取账户信息。</span>`,
            },
            {
                prependAvatar: 'AY.png',
                title: '遨游图书馆',
                href: "http://www.allinit.cn/",
                target: "_blank",
                subtitle: `<span>公司已有账号，可在群公告获取账户信息。</span>`,
            },
            {
                prependAvatar: 'GOOGLE.png',
                title: '谷粉学术',
                href: "http://xueshu.99lb.net/",
                target: "_blank",
                subtitle: `<span>口令gfsoso。</span>`,
            },

        ]
    },
    {
        title: "数据网站", childen: [
            {
                prependAvatar: 'GJTJJ.ico',
                title: '国家统计局',
                href: "https://data.stats.gov.cn/",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★★★</span>`,
            },
            {
                prependAvatar: 'https://www.gtarsc.com/favicon.png',
                title: '国泰安、统计年鉴、RESSET锐思',
                href: "http://www.520myfuture.com/db/entrance/?catId=20",
                target: "_blank",
                subtitle: `<span>已买账号<br/>推荐指数：★★★★★</span>`,
            },
            {
                prependAvatar: 'http://www.cbirc.gov.cn//cn/static/favicon.ico',
                title: '中国银保监会',
                href: "http://www.cbirc.gov.cn/cn/view/pages/tongjishuju/tongjishuju.html",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: 'https://data.eastmoney.com/favicon.ico',
                title: '东方财富网',
                href: "https://data.eastmoney.com/report/",
                target: "_blank",
                subtitle: `<span>可复制数据<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: '/tools-next/IDA.png',
                title: '世界银行公开数据',
                href: "https://data.worldbank.org.cn/",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'http://u.thsi.cn/2013/08/07/162606854_1375865250_-1408208115_685afc5431c9b7b3.png',
                title: '同花顺',
                href: "https://www.10jqka.com.cn/",
                target: "_blank",
                subtitle: `<span>可复制数据<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: 'INE.png',
                title: '上海国际能源交易中心',
                href: "https://www.ine.cn/",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'SWB.png',
                title: '中华人民共和国商务部',
                href: "https://www.ine.cn/",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://uqer.datayes.com/img_home/favicon.ico',
                title: '优矿',
                href: "https://uqer.datayes.com/",
                target: "_blank",
                subtitle: `<span>免费（简单代码）<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'SWGC.png',
                title: '数位观察',
                href: "https://www.swguancha.com/",
                target: "_blank",
                subtitle: `<span>部分免费<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'SHHJNY.png',
                title: '上海环境能源交易所',
                href: "https://www.cneeex.com/",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'GMS.png',
                title: '世界数据图册',
                href: "https://cn.knoema.com/atlas",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★</span>`,
            },

        ]
    },
    {
        title: "研报网站", childen: [
            {
                prependAvatar: 'https://report.iresearch.cn/include/public/images/favicon.ico',
                title: '艾瑞网',
                href: "https://report.iresearch.cn/",
                target: "_blank",
                subtitle: `<span>部分免费<br/>推荐指数：★★★★★</span>`,
            },
            {
                prependAvatar: 'PDCP.png',
                title: '全国图书馆参考咨询联盟',
                href: "http://www.ucdrs.net/",
                target: "_blank",
                subtitle: `<span>免费，发送邮箱<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: 'IBM.png',
                title: 'IBM商业价值研究院',
                href: "https://www.ibm.com/cn-zh/services/insights",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: 'http://static.cninfo.com.cn/new/img/favicon.ico',
                title: '巨潮资讯',
                href: "http://www.cninfo.com.cn/new/index",
                target: "_blank",
                subtitle: `<span>注册后免费下载<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: 'CAICT.png',
                title: '中国信通院',
                href: "http://www.caict.ac.cn/",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: 'https://www2.jiumodiary.com/images/front/eleps.png',
                title: '鸠摩文档搜索',
                href: "https://www.jiumosearch.com/",
                target: "_blank",
                subtitle: `<span>免费，登录百度网盘，每天100本<br/>推荐指数：★★★★</span>`,
            },
            {
                prependAvatar: 'https://img1.dydata.io/static/images/icon/favicon.ico',
                title: '镝数聚',
                href: "https://www.dydata.io/",
                target: "_blank",
                subtitle: `<span>部分免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://36kr.com/favicon.ico',
                title: '36kr研究院',
                href: "https://36kr.com/academe",
                target: "_blank",
                subtitle: `<span>行业报告<br/>注册后免费下载<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.chinaventure.com.cn/images/logo/logo_tiny.png',
                title: '投中网',
                href: "https://www.chinaventure.com.cn/report/list.html",
                target: "_blank",
                subtitle: `<span>行业报告<br/>部分免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.amac.org.cn/favicon.ico',
                title: '中国证券投资基金协会',
                href: "https://www.amac.org.cn/",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'http://www.cnnic.net.cn/images/logo.jpg',
                title: '中国互联网络信息中心',
                href: "http://www.cnnic.net.cn/",
                target: "_blank",
                subtitle: `<span>免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.djyanbao.com/favicon.ico',
                title: '洞见报告',
                href: "https://www.djyanbao.com/index",
                target: "_blank",
                subtitle: `<span>部分免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://51bmj.cn/favicon.ico',
                title: '比目镜',
                href: "https://www.51bmj.cn/",
                target: "_blank",
                subtitle: `<span>部分免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.chacewang.com/favicon.ico',
                title: '查策网',
                href: "https://www.chacewang.com/",
                target: "_blank",
                subtitle: `<span>部分免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.fxbaogao.com/favicon.ico',
                title: '发现报告',
                href: "https://www.fxbaogao.com/",
                target: "_blank",
                subtitle: `<span>部分免费<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.xuexi.cn/favicon.ico',
                title: '学习强国',
                href: "https://www.xuexi.cn/",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.gov.cn/govweb/xhtml/2016gov/images/public/logo.jpg',
                title: '中国政府网',
                href: "https://www.gov.cn/",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★★</span>`,
            },
            {
                prependAvatar: 'https://www.camet.org.cn/r/cms/www/default/static/images/favicon.ico',
                title: '中国城市轨道交通协会',
                href: "https://www.camet.org.cn/xytj",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'YG.ico',
                title: '易观',
                href: "https://www.analysys.cn/",
                target: "_blank",
                subtitle: `<span>注册后查看报告<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'KJDS.png',
                title: '跨境电商网',
                href: "http://www.100ec.cn/zt/wmds/",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'CNCIC.png',
                title: '中华全国商业信息中心',
                href: "https://www.cncic.org/",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'BDR.ico',
                title: '比达网',
                href: "https://www.jiumosearch.com/",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★</span>`,
            },
            {
                prependAvatar: 'ST.png',
                title: '速途研究院',
                href: "http://www.sootoo.com/keyword/157613",
                target: "_blank",
                subtitle: `<span>仅查看<br/>推荐指数：★★</span>`,
            },
        ]
    },

]
</script>

