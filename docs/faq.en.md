---
comments: true
---


#### Q: After setting up the environment and running `python main.py`, an error message appears: **OSError: [WinError 126] The specified module could not be found**

**A**: The reason is that the Shapely library is not installed correctly. If you are using Windows, you can download the corresponding whl package from [Shapely whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) and use the offline installer. Another option is to install it using conda. (@[hongyuntw](https://github.com/hongyuntw))
