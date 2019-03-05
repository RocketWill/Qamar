//获取应用实例
var app = getApp();
Page({
    data: {
    },
    onLoad() {

    },
    onShow() {
        let that = this;
        that.setData({
            user_info: {
                nickname: "卡數洞",
                avatar_url: "/images/more/logo.png"
            },
        })

        wx.request({
            url: app.buildUrl("/get-member-info"),
            method: "POST",
            data: {"token": app.getCache("token")},
            header: app.getRequestHeader(),
            success: function (res) {
                console.log(res);
                if (res.data.code == 200) {
                    that.setData({
                        user_info : res.data.member,
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
    emailValid: function () {
        wx.navigateTo({
          url: "/pages/email/index"
        });
      },
});