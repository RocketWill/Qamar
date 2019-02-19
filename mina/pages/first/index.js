//index.js
//获取应用实例
var app = getApp()
Page({

  data: {
    qu: [{
      'title': "獲取問題列表時出錯",
      'content': "請確認網絡情況後重試"
    }],
    date: "10月26日 周三",
    items: [{
      message: 'foo',
    }, {
      message: 'bar'
    }],
    imgUrls: [{
        url: 'http://img.hb.aicdn.com/42f1c1bfc23929cc35fedc5d7f364b749973ed33ad2be-FXvuhX',
        txt1: "当我们17岁",
        txt2: "爱恨都来得莫名其妙"
      },
      {
        url: 'http://img.hb.aicdn.com/4649bf98371c7e900c93e772f5a26f6223933744a3602-o1p1o2',
        txt1: "耶稣基督：走出埃及 ",
        txt2: "上帝之子耶稣"
      },
      {
        url: 'http://img.hb.aicdn.com/2397ca2a6c0ee445f20949aaa3bd4cc9b7188e496ae95-crz27s',
        txt1: "无伴奏 無伴奏",
        txt2: "我只是喜欢那个貌似全世界少年人都疯狂的年代"
      }
    ],
    indicatorDots: true,
    autoplay: true,
    interval: 5000,
    duration: 500,
    categories: [{
        id: 0,
        name: "最熱門"
      },
      {
        id: 1,
        name: "最實用"
      },
      {
        id: 2,
        name: "今日火熱"
      },
      {
        id: 3,
        name: "最熱門"
      },
      {
        id: 4,
        name: "最實用"
      },
      {
        id: 5,
        name: "今日火熱"
      },
    ],
    activeCategoryId: 3,
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onPullDownRefresh() {
    this.getQuestionList();
  },
  toAsk: function() {
    wx.navigateTo({
      url: '/pages/question-ask/question-ask',
    });
  },

  getQuestionList: function(){
    var that = this;
    
    wx.request({
      url: app.buildUrl("/get-content"),
      method: "POST",
      data: {
        'action': "get_content"
      },
      header: app.getRequestHeader(),
      success: function (res) {
        if (res.data.code == 200) {
          that.setData({
            qu: res.data.data[0],
            date: res.data.date
          });
        } else {
          that.setData({
            qu: [{
              'title': "獲取問題列表出錯",
              'content': ""
            }]
          });
        }
      }
    });
  },

  onLoad: function() {
    wx.setNavigationBarTitle({
      title: app.globalData.appName
    });

    this.getQuestionList();
  },

  onShow: function () {
    this.getQuestionList();
  },
})