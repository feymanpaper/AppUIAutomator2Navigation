## 环境配置
配置uiautomator2环境:https://github.com/openatx/uiautomator2

## 运行
在Config.py中更改要测试的包名
```commandline
self.target_pkg_name = "com.example.packagename"
```
运行run.py

## 遍历思路
### 点击过程
对于一个界面，会遍历当前界面的所有可点击组件进行依次点击，
由于点击之后可能会触达新的界面，因此需要在点击之前维护当前界面的上下文，
如当前界面的界面信息(文本, 位置), 当前界面已经点击了哪些组件...

每到达一个界面, 我们会将当前界面的界面信息(文本, 组件位置等)和Memory(存储之前遍历过的界面信息)
进行相似度比较, 如果相似度大于阈值, 认为当前界面是一个已经存在的界面(ExistScreen), 否则认为是一个新的界面(NewScreen)。
取出当前界面的上下文后，从上次点击未完成的组件开始继续点击。如果当前界面已经点击完成, 就触发
press back回退, 到上一层界面进行点击, 重复上述流程。

一个可点击组件点击完成的定义: 该组件不会产生页面跳转 或 该组件对应的下一跳界面点击完成  
一个界面点击完成的定义: 该界面所有可点击组件均点击完成

### 状态检测
定义了以下状态:
| 状态     | 描述 |对应处理|
| ----------- | ----------- | ----------- |
| STATE_ExitApp      | 当前跳出了测试App       |press back回退到测试App|
| STATE_InputMethod   | 当前遇到输入法        |press back退出输入法|
| STATE_ExistScreen   | 当前界面已经存在        |取出当前界面上下文并继续点击|
| STATE_FinishScreen   | 当前界面点击完成        |press back回退到上一层界面|
| STATE_NewScreen   | 当前界面为新触达界面        |为新界面分配上下文并且加入到App界面跳转图, 开始点击|
| STATE_WebViewScreen   | 当前界面为WebView        |press back回退到上一层界面|

### 去重过程
每到达一个界面, 我们会将当前界面的界面信息(文本, 组件位置等)和Memory(存储之前遍历过的界面信息)
进行相似度比较, 如果相似度大于某个阈值, 认为当前界面是一个已经存在的界面, 没必要认为是一个新
界面, 则取出该界面的上下文继续进行点击。

当然目前的去重方法还不是特别有效, 比如类似淘宝的商品界面, 点进去基本是无穷无尽, 也是目前
遇到的阻碍。目前的一个思路是hook url, 能否根据url的信息来对界面进行去重, 是目前正在尝试的思路。

### 提高覆盖率的思路
若对每个组件只允许点击一次，会造成许多界面无法遍历到。
因此程序会记录每个可点击组件触达的下一个界面nextScreen。若nextScreen没点击完成，
将继续点击该组件跳转到nextScreen去继续点击。同时会检测回边/环的情况, 避免进入到死循环。

### 容错机制
错误的发生往往是在当前界面所有组件已经点击完毕，
应当press back回退到上一层界面。此时可能会遇到弹框或回退无效等卡住的情况。
这种情况下程序将触发1.随机点机制，从可能产生界面跳转的组件中随机选择一个组件点击。
2.若还是不能回退, 则重启测试app，并且记录卡住的界面和触达该界面所点击的组件，
以避免重启之后再次点击。

### 隐私导向
每个界面维护一个可点击组件的List，在加入可点击组件的过程中，如果该可点击组件的文本与隐私相关，
则从List头部加入，否则从尾部加入。保证隐私相关组件优先点击




