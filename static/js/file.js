 var sendMessage = function (url,data,reject,resolve) {
        $.ajax({
            //请求方式
            type : "POST",
            //请求的媒体类型
            contentType: "application/x-www-form-urlencoded;charset=UTF-8",
            //请求地址
            url : url,
            //数据，json字符串
            data : JSON.stringify(data),
            //请求成功
            success : function(result) {
                reject(result)
            },
            //请求失败，包含具体的错误信息
            error : function(e){
                resolve(e)
            }
        });
    };
