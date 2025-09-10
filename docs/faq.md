---
comments: true
---

#### Q: 装完环境之后，运行`python main.py`之后，报错**OSError: [WinError 126] 找不到指定的模組**

**A**: 原因是Shapely库没有正确安装，如果是在Windows，可以在[Shapely whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)下载对应的whl包，离线安装即可；另外一种解决办法是用conda安装也可。(@[hongyuntw](https://github.com/hongyuntw))
