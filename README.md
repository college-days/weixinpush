### 用于微信公共平台的主动消息推送

* 通过解析浏览器端的请求实现
* 获取用户数量和获取用户ID由于腾讯在前段做了处理，所以只能是用正则解析
* 只是一个主动推送脚本，可以单独运行也可以和现有的微信框架整合在一起
* 第一次主动推送貌似需要用户回复一条信息才能让用户收到，提示信息会在脚本执行后在shell中显示

### requirement

* python 2.7.x
* requests

### settings

* 在login()的loginParams中填入username和password，参数值第一次可以通过抓包来分析

### common bugs

* getUserCount() 在使用两次pushSingleMsg()会出现bug崩溃，有待调试
