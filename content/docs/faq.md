---
weight: 5000
lastmod: "2022-10-08"
draft: false
author: "SWHL"
title: "常见问题"
icon: "update"
toc: true
description: ""
---

#### Q: 装完环境之后，运行`python main.py`之后，报错**OSError: [WinError 126] 找不到指定的模組**
**A**: 原因是Shapely库没有正确安装，如果是在Windows，可以在[Shapely whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)下载对应的whl包，离线安装即可；另外一种解决办法是用conda安装也可。(@[hongyuntw](https://github.com/hongyuntw))


<script src="https://giscus.app/client.js"
        data-repo="SWHL/RapidVideOCR"
        data-repo-id="MDEwOlJlcG9zaXRvcnk0MDU1ODkwMjk="
        data-category="Q&A"
        data-category-id="DIC_kwDOGCzMJc4CUluM"
        data-mapping="title"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>