
//获取应用实例
var app = getApp();

Page({
    data: {
        email: undefined,

    },
    onShow: function () {
        var that = this;
    },
    onLoad: function (e) {
        var that = this;
    },
    createOrder: function (e) {
        wx.showLoading();
        var that = this;
        wx.navigateTo({
            url: "/pages/my/order_list"
        });
    },
    goToIndex: function () {
        wx.switchTab({
            url: '/pages/food/index',
        });
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },
    emailInputEvent: function (e) {
        this.setData({
            email: e.detail.value
        })
    },
    isNumberOr_Letter: function (s) {

        var regu = "^[0-9]{10}$";
        var re = new RegExp(regu);
        if (re.test(s)) {
            return true;
        } else {
            return false;
        }
    },
    showBusy: function () {
        wx.showToast({
            title: '處理中...',
            mask: true,
            icon: 'loading'
        })
    },


    emailValidation: function () {
        var that = this;

        console.log(that.data.email);
        if (this.isNumberOr_Letter(that.data.email) == false) {
            app.alert({'content': "郵箱格式錯誤，請重試"});
            return;
        }
        var data = {'email': that.data.email, "key": app.getCache("token")};
        wx.showLoading({
            title: '全力處理中',
        })

        wx.request({
            url: "http://127.0.0.1:8999/mail/validation",
            method: "POST",
            data: data,
            header: app.getRequestHeader(),
            success: function (res) {
                wx.hideLoading();
                console.log(res);
                if (res.data.code == 200) {
                    app.alert({
                        'content': res.data.msg,
                        'cb_confirm': function () {
                            that.goToIndex()
                        }
                    });
                    //return;
                }
                if (res.data.code == -1) {
                    app.alert({
                        'content': res.data.msg
                    });
                    //return;
                }

                //app.setCache("token", res.data.data.token);

            }
        });
    },
    uploadPhoto: function () {
        var that = this;
        wx.chooseImage({
            count: 1, // 默认9
            sizeType: ['compressed'], // 可以指定是原图还是压缩图，默认二者都有
            sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
            success: function (res) {
                // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
                var tempFilePaths = res.tempFilePaths;
                that.upload(that, tempFilePaths);
            }
        })
    },

    upload: function (page, path) {
        wx.showToast({
            icon: "loading",
            title: "正在上传"
        }),
            wx.uploadFile({
                url: app.buildUrl("/get-question"),
                filePath: path[0],
                name: 'file',
                header: { "Content-Type": "multipart/form-data" },
                formData: {
                    //和服务器约定的token, 一般也可以放在header中
                    'session_token': app.getCache('token')
                },
                success: function (res) {
                    console.log(res);
                    if (res.statusCode != 200) {
                        wx.showModal({
                            title: '提示',
                            content: '上传失败',
                            showCancel: false
                        })
                        return;
                    }
                    var data = res.data
                    page.setData({  //上传成功修改显示头像
                        src: path[0]
                    })
                },
                fail: function (e) {
                    console.log(e);
                    wx.showModal({
                        title: '提示',
                        content: '上传失败',
                        showCancel: false
                    })
                },
                complete: function () {
                    wx.hideToast();  //隐藏Toast
                }
            })
    }

});
