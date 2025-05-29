---
weight: 3501
title: "初级教程（界面版 下载解压使用）"
description: ""
icon: local_library
date: 2023-10-08
draft: false
---

#### 引言

- 考虑到提取视频字幕的小伙伴大多不是程序员行当，为了降低使用门槛，特此推出界面版的RapidVideOCR Desktop.
- RapidVideOCR Desktop需要搭配VideoSubFinder使用。它们两个关系如下图所示：

    ```mermaid
    flowchart LR
       A(VideoSubFinder) --提取字幕关键帧--> B(RapidVideOCR)  --OCR--> C(SRT)
   ```

#### [VideoSubFinder使用教程](https://blog.csdn.net/shiwanghualuo/article/details/129174857)

#### RapidVideOCR Desktop使用教程

1. 下载对应平台的**RapidVideOCR Desktop**压缩包
   - [Github下载最新版本](https://github.com/SWHL/RapidVideOCRDesktop/releases)
   - QQ群共享文件下载，QQ群号：706807542， 或者扫码加入：
    <div align="center">
        <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/QQGroup.png" width="15%" height="15%" align="center">
    </div>
2. 解压zip包，双击`RapidVideOCR.exe`（以Windows平台为例）
3. 界面如下图所示：
    <div align="center">
        <img src="https://github.com/SWHL/RapidVideOCR/releases/download/v2.0.1/DesktopUI.png" width=50%>
    </div>

4. 界面各个部分介绍
    - RapidVideOCR:
        - **图像目录**：指的是**VideoSubFinder**软件生成的**RGBImages**或者**TXTImages**目录，必须是这两个目录之一
        - **保存路径**：识别转换后的结果，包括srt文件、ass文件、和txt文件
        - **叠图识别**：勾选后，识别速度会变快。准确率可能差些
    - VideoSubFinder + RapidVideOCR:
        - **VSF exe路径**：本地安装的VideoSubFinder全路径，例如:`G:\ProgramFiles\VideoSubFinder_6.10_x64\Release_x64\VideoSubFinderWXW.exe`
        - **视频目录**：想要提取硬字幕的视频所在目录
        - **保存路径**：保存提取结果的目录
6. 上述都填好之后，点击OK按钮，即可开始识别。

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
