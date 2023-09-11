console.log("Script loaded successfully ");
Java.perform(function x() {
    // hook Intent之间传递的url
    var act = Java.use("android.content.Intent");

    act.getData.implementation = function() {
        var data = this.getData()
        var extra = this.getExtras()
        send(data)
        send(extra.toString())
        send(this.toUri(256))
        return data
    };

     act.getData.implementation = function() {
        var data = this.getData()
        var extra = this.getExtras()
        send(data)
        send(extra.toString())
        send(this.toUri(256))
        return data
    };
    // hook startActivity传递的url
    var Activity = Java.use("android.app.Activity");
    Activity.startActivity.overload('android.content.Intent').implementation=function(p1){
        var data = decodeURIComponent(p1.toUri(256))
        send(data)
        this.startActivity(p1);
    }
    Activity.startActivity.overload('android.content.Intent', 'android.os.Bundle').implementation=function(p1,p2){
        var data = decodeURIComponent(p1.toUri(256))
        send(data)
        this.startActivity(p1,p2);
    }

    var Window = Java.use("android.view.Window");
    Window.setFlags.implementation = function(flags, mask){
        // 将 FLAG_SECURE 参数更改为 0
        var newFlags = flags & ~WindowManager.LayoutParams.FLAG_SECURE;
        // 调用原始方法
        this.setFlags(newFlags, mask);
    }

    var Webview = Java.use("android.webkit.WebView")
        Webview.loadUrl.overload("java.lang.String").implementation = function(url) {
        send("[+]Loading URL from", url);
        this.loadUrl.overload("java.lang.String").call(this, url);
    }
//
//    Java.choose('android.webkit.WebView',{
//        onMatch: function (instance) {
//            console.log("Found instance: " + instance);
//            console.log("URL: "+instance.getUrl());
//        },
//        onComplete: function () {
//            console.log('Finished')
//        }
//    });

});


//console.log("Script loaded successfully ");
//
//function callSecretFun() { //定义导出函数
//    Java.perform(function () { //找到隐藏函数并且调用
//        Java.choose("android.content.Intent", {
//            onMatch: function (instance) {
//                console.log("Found intent: " + instance);
//                console.log("Data: " + instance.getData());
//                console.log("Extras: " + instance.getExtras())
//                console.log("\n")
//            },
//            onComplete: function () { }
//        });
//    });
//}
//rpc.exports = {
//    callsecretfunction: callSecretFun //把callSecretFun函数导出为callsecretfunction符号，导出名不可以有大写字母或者下划线
//};