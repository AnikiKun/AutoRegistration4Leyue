## 基于Python的自动挂号机器

有两套脚本，代码基本一致，一套是基于Webdriver，通过chrome来完成挂号。
一套是基于PhantonJS的无头版本。

脚本中都是针对portal.leyue.com该挂号站点进行开发的。
开源仅供参考学习，如果对web自动化有兴趣的同学可以参考学习。

已经实现的功能和效果：
- 自动登录
- cookie自动填充
- 号源信息提取、号源为空时自动刷新，可用来监控偶尔放出来的号源
- 自动挂号，当出现多个号源时，支持同时打开多个浏览器自动挂号

由于手动抢号一直失败，故而开发了这套脚本。本质上是为了偷懒，请勿用来做不合法的事情。


## 使用方法

- 1、下载项目
- 2、安装python
- 3、安装pip
- 4、安装Selenium
- 5、安装chrome浏览器
- 6、安装chromedriver
- 7、执行代码

### 补充

```python
self.userName = 'xxxx'  # 登录乐约平台的用户名
self.password = 'xxxx'  # 密码
self.host = 'http://portal.leyue100.com'   # 不用改
self.doctorPageUrl = 'url'   # 需要挂号的医生的页面地址
```
