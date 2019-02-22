//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
    regFlag: true
  },
  goToIndex: function() {
    wx.navigateTo({
      url: '/pages/food/index',
    });
  },
  goToIndex2: function() {
    wx.switchTab({
      url: "/pages/first/index"
    });
  },
  onLoad: function() {
    wx.setNavigationBarTitle({
      title: app.globalData.appName
    });
    this.checkLogin();
  },
  onShow: function() {
    //獲取個人問題列表＆回覆
    this.getMyQuestion();

  },
  onReady: function() {
    var that = this;
    setTimeout(function() {
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function(res) {
      var angle = -(res.x * 30).toFixed(1);
      if (angle > 14) {
        angle = 14;
      } else if (angle < -14) {
        angle = -14;
      }
      if (that.data.angle !== angle) {
        that.setData({
          angle: angle
        });
      }
    });
  },
  checkLogin: function() {
    var that = this;
    wx.login({
      success: function(res) {
        if (!res.code) {
          app.alert({
            'content': '登錄失敗，請再次點擊'
          });
          return;
        }

        wx.request({
          url: app.buildUrl("/member/check-reg"),
          method: "POST",
          data: {
            code: res.code
          },
          header: app.getRequestHeader(),
          success: function(res) {
            //console.log(res);
            if (res.data.code != 200) {
              that.setData({
                regFlag: false
              });
            }
            app.setCache("token", res.data.data.token);
            //that.goToIndex();
          }
        });
      }
    });
  },
  login: function(e) {
    var that = this;
    //console.log(e);
    if (!e.detail.userInfo) {
      app.alert({
        'content': '登錄失敗，請再次點擊'
      });
      return;
    }

    var data = e.detail.userInfo;

    wx.login({
      success: function(res) {
        if (!res.code) {
          app.alert({
            'content': '登錄失敗，請再次點擊'
          });
          return;
        }

        data['code'] = res.code;

        wx.request({
          url: app.buildUrl("/member/login"),
          method: "POST",
          data: data,
          header: app.getRequestHeader(),
          success: function(res) {
            if (res.data.code != 200) {
              app.alert({
                'content': res.data.msg
              });
              return;
            }
            app.setCache("token", res.data.data.token);
            that.goToIndex();
          }
        });
      }
    });


  },

  getMyQuestion: function() {
    const token = app.getCache('token');
    console.log(token);
    wx.request({
      url: app.buildUrl("/get-my-question"),
      method: "POST",
      data: {'token':token},
      header: app.getRequestHeader(),
      success: function (res) {
        if (res.data.code != 200) {
          app.alert({
            'content': res.data.msg
          });
          return;
        }
      }
    });
  }
});