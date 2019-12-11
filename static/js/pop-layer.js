/**
 * 成功时 Alert框
 * @param tipsStr  提示信息，
 * @param isReloadPage  是否重新加载Alert的父页面
 */
function successLayerAlert(tipsStr, isReloadPage) {
    layer.alert(tipsStr, {
        skin: 'layui-layer-molv',//样式类名  自定义样式
        closeBtn: 1,  // 是否显示关闭按钮
        anim: 1, //动画类型
        btn: ['好的'], //按钮
        icon: 6,  // icon
        yes: function (index) {
            if (isReloadPage) {
                window.location.reload();//刷新页面
            }
            layer.close(index);  //关闭 layer.alert
        }
    });
}

/**
 * 发生错误时 Alert框
 * @param tipsStr  提示信息，
 * @param isReloadPage 是否重新加载Alert的父页面
 */
function failLayerAlert(tipsStr, isReloadPage) {
    layer.alert(tipsStr, {
        skin: 'layui-layer-molv',//样式类名  自定义样式
        closeBtn: 1,  // 是否显示关闭按钮
        anim: 1, //动画类型
        btn: ['确定', '气一会儿'], //按钮
        icon: 5,  // icon
        yes: function (index) {
            if (isReloadPage) {
                window.location.reload();//刷新页面
            }
            layer.close(index);  //关闭 layer.alert
        },
        btn2: function (index) {
            if (isReloadPage) {
                window.location.reload();//刷新页面
            }
            layer.close(index);//关闭 layer.alert
        }
    });
}


/*******************************************
 **添加成员弹出层 js start
 *******************************************/
/**
 * 添加成员弹出层
 * @param pageurl 弹出层路径
 * @param  submiturl  弹出层数据提交路径
 */
var addDepartLayer = function (pageurl, submiturl,initial) {
    layer.open({
        type: 2,//2表示弹出框类型
        title: '添加成员',
        skin: 'CLYM-style',
        btn: ['确定', '取消'],
        maxmin: false,
        area: ['456px', '560px'],
        shift: 1,//弹出框动画效果
        scrollbar: false, // 父页面 滚动条 禁止
        content: pageurl,
        //确定按钮被点击 ,index 当前层索引 layero 当前层的doc 顺序和success的相反
        yes: function (index, layero) {
            //获取子窗口中iframe中id为fmcollection的表格文本
            let formdocument = $(layero).find("iframe")[0].contentWindow.document.getElementById("fm");
            let name = formdocument["name"].value;
            initial = formdocument["initial"].value;
            if (name === '') {
                layer.msg('姓名为空');
                return
            } else if (initial === '') {
                layer.msg('姓名拼音缩写为空');
                return
            }
            let data = {
                'name': name,
                'initial': initial
            };
            sendMessage(submiturl, data, function (res) {

               let resp = res;
                let success = resp['success'];
                if (success) {
                    let ct = resp['context'];
                    let msg = ct['msg'];
                    layer.close(index);
                    successLayerAlert(msg, true);
                    collectionInfoLayer('/video_collection_info_layer','/video_collection_info',initial)
                } else {
                    let ct = resp['context'];
                    let msg = ct['msg'];
                    failLayerAlert(msg, false);
                }
            }, function (e) {
                failLayerAlert('发送失败!', false);
            })
        },
        btn2: function (index, layero) {
        },
        //弹出界面成功后执行
        success: function (layero, index) {
        },
        //layer结束时调用
        end: function () {
        }
    })
};

/********************************************
 **添加成员弹出层 js end
 *******************************************/


/*******************************************
 **修改成员弹出层 js start
 *******************************************/
/**
 * 修改成员弹出层
 * @param pageurl 弹出层路径
 * @param  submiturl  弹出层数据提交路径
 * @param  initial  需要修改的id
 */
var collectionInfoLayer = function (pageurl, submiturl,initial) {
    layer.open({
        type: 2,//2表示弹出框类型
        title: '信息采集成员',
        skin: 'CLYM-style',
        btn: ['确定', '取消'],
        maxmin: false,
        area: ['456px', '560px'],
        shift: 1,//弹出框动画效果
        scrollbar: false, // 父页面 滚动条 禁止
        content: pageurl+'?initial='+initial,
        //确定按钮被点击 ,index 当前层索引 layero 当前层的doc 顺序和success的相反
        yes: function (index, layero) {

            let iframeWin=window[layero.find('iframe')[0]['name']];//得到layero doc 中iframe 页的窗口对象
            iframeWin.stopCllocetion(); //调用子窗口的函数来停止
            //获取子窗口中iframe中id为fm的表格文本
            // let formdocument = $(layero).find("iframe")[0].contentWindow.document.getElementById("fm");

        },
        btn2: function (index, layero) {
            let iframeWin=window[layero.find('iframe')[0]['name']];//得到layero doc 中iframe 页的窗口对象
            iframeWin.stopCllocetion(); //调用子窗口的函数来停止
        },
        //弹出界面成功后执行
        success: function (layero, index) {
            let iframeWin=window[layero.find('iframe')[0]['name']];//得到layero doc 中iframe 页的窗口对象
            iframeWin.childFunction(initial); //调用子窗口的函数来传
        },
        //layer结束时调用
        end: function () {
        }
    })
};

/********************************************
 **修改成员弹出层 js end
 *******************************************/





/*******************************************
 **修改成员弹出层 js start
 *******************************************/
/**
 * 修改成员弹出层
 * @param pageurl 弹出层路径
 * @param  submiturl  弹出层数据提交路径
 * @param  id  需要修改的id
 * @param  depart_name  需要修改的名字
 */
var editDepartLayer = function (pageurl, submiturl, id, depart_name) {
    layer.open({
        type: 2,//2表示弹出框类型
        title: '编辑成员',
        skin: 'CLYM-style',
        btn: ['确定', '取消'],
        maxmin: false,
        area: ['456px', '560px'],
        shift: 1,//弹出框动画效果
        scrollbar: false, // 父页面 滚动条 禁止
        content: pageurl,
        //确定按钮被点击 ,index 当前层索引 layero 当前层的doc 顺序和success的相反
        yes: function (index, layero) {
            //获取子窗口中iframe中id为fm的表格文本
            let formdocument = $(layero).find("iframe")[0].contentWindow.document.getElementById("fm");
            //获取表单内需要传送的值
            let name = formdocument["name"].value;
            let id = formdocument["id"].value;

            if (name === '') {
                layer.msg('姓名为空');
                return
            }
            let data = {
                'id': id,
                'name': name,
            };
            sendMessage(submiturl, data, function (res) {
                let resp = res;
                let success = resp['success'];
                if (success) {
                    let ct = resp['context'];
                    let msg = ct['msg'];
                    layer.close(index);
                    successLayerAlert(msg, true);
                } else {
                    let ct = resp['context'];
                    let msg = ct['msg'];
                    failLayerAlert(msg, false);
                }
            }, function (e) {
                failLayerAlert('发送失败!', false);
            })
        },
        btn2: function (index, layero) {
        },
        //弹出界面成功后执行
        success: function (layero, index) {
            let iframeWin = window[layero.find('iframe')[0]['name']];//得到layero doc 中iframe 页的窗口对象
            iframeWin.setValue(id, depart_name)
        },
        //layer结束时调用
        end: function () {
        }
    })
};

/********************************************
 **修改成员弹出层 js end
 *******************************************/

var deleteDepart = function (url, id) {
    let strTip = "确定<span style='color:red;'>删除?</span>";
    layer.confirm(strTip, {btn: ["确定", "算了"], title: "警告", icon: 3}, function (index) {
        let layerIndex = layer.msg("正在删除,请稍后!!", {
            shadeClose: false,//点击遮罩层不关闭
            time: 60000,//60秒后自动关闭
            icon: 16, // 0~2 ,0比较好看
            shade: [0.5, 'black'] // 黑色透明度0.5背景
        });
        let jsondata = {
            'id': id
        };
        sendMessage(url, jsondata, function (res) {
            let data = res;
            if (data.success) {
                layer.close(layerIndex);
                successLayerAlert("删除成功!",true);
            } else {
                layer.close(layerIndex);
                let ct = data.context;
                let msg = ct.msg;
                failLayerAlert(msg, false);
            }


        }, function (e) {

        });
    });
};
var trainModel = function (url) {
    let strTip = "训练可能花费一段时间，确定<span style='color:red;'>训练?</span>";
    layer.confirm(strTip, {btn: ["确定", "算了"], title: "警告", icon: 3}, function (index) {
        let layerIndex = layer.msg("正在训练,请稍后!!", {
            shadeClose: false,//点击遮罩层不关闭
            time: 80000,//60秒后自动关闭
            icon: 16, // 0~2 ,0比较好看
            shade: [0.5, 'black'] // 黑色透明度0.5背景
        });

        sendMessage(url, {}, function (res) {
            let data = res;
            if (data.success) {
                layer.close(layerIndex);
                successLayerAlert("训练成功!",true);
            } else {
                layer.close(layerIndex);
                let ct = data.context;
                let msg = ct.msg;
                failLayerAlert(msg, false);
            }


        }, function (e) {

        });
    });
};