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
            url: '/pages/first/index',
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
        if (this.isNumberOr_Letter(that.data.email) == false){
            app.alert({'content':"郵箱格式錯誤，請重試"});
            return;
        }
        var data = {'email': that.data.email, "key": app.getCache("token")};
        wx.showLoading({
            title: '全力處理中',
        })

        wx.request({
            url:"http://127.0.0.1:8999/mail/validation",
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
    }

});
