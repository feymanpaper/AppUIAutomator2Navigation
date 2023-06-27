### 运行
在Config.py中设置要跑的app的路径
```commandline
self.app_path = "E:\\app\\"
```
在Config.py中设置跑出来的数据存放地址
```commandline
self.app_data_path = "G:\\app_audit\\"
```
运行run.py，然后。。。。睡觉

运行完成后，在app_path会有运行的结果。

比较重要的是里面那个json文件

每个节点的ck_eles_text为界面的唯一标识：ck_eles_text

ck_eles_text通过下面这个代码编码转化后就是在文件夹里面存储的截屏和xml文件的名字
```python
    def get_hash(self, ck_eles_text):
        data_sha = hashlib.sha256(ck_eles_text.encode('utf-8')).hexdigest()
        return data_sha
```

每个节点的call_map存有当前界面的下一个界面，可能会有多个下一个界面
```commandline
"call_map": {
      ".MainActivityV2-tv.danmaku.bili-android.widget.TextView-tv.danmaku.bili:id/disagree-(539,1589)-不同意": "hash"
}
```
其中key就是：下一个界面的activity name - 跳转点击的坐标位置 - 文本
value就是ck_eles_text（上面这个例子我简单写成hash，具体看一看实际的例子）

跑出来的数据例子可以参考下目录里的case文件夹

要跑的app我已经放到了服务器1里面的：/data/gosec/app300

TODO： 画一个调用图

