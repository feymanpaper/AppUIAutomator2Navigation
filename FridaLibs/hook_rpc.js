console.log("Script loaded successfully ");
Java.perform(function x() {
    var act = Java.use("android.content.Intent");
    act.getData.implementation = function() {
        var data = this.getData()
        var extra = this.getExtras()
//        if(extra === null || JSON.stringify(extra)=="{}"){
//            return data.toString()
//        }
//        if(data === null || JSON.stringify(data) == "{}"){
//            return data.toString()
//        }
//        if(extra === null){
//            return data
//        }

        send(data)
        send(extra.toString())
        return data
    };

     act.getData.implementation = function() {
        var data = this.getData()
        var extra = this.getExtras()
//        if(extra === null || JSON.stringify(extra)=="{}"){
//            return data.toString()
//        }
//        if(data === null || JSON.stringify(data) == "{}"){
//            return data.toString()
//        }

//        if(extra === null){
//            return data
//        }
        send(data)
        send(extra.toString())
        return data
    };

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