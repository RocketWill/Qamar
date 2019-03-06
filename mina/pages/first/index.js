//index.js
//获取应用实例
var app = getApp()
Page({

  data: {
    qu: [{
      'title': "獲取問題列表時出錯",
      'content': "請確認網絡情況後重試"
    }],
    select: false,
    search_kw:"",
    cat:[],
    cat_id:0,
    date: "10月26日 周三",
    qid:"",
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
        name: "官方回覆"
      },
      {
        id: 1,
        name: "本週熱門"
      },
      {
        id: 2,
        name: "尚未解答"
      },
      {
        id: 3,
        name: "歷史火熱"
      },
      {
        id: 4,
        name: "所有問題"
      },
      
    ],
    activeCategoryId: 4,
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  toReply:function(e){
    var that = this;
    var qid = ""+e.currentTarget.dataset.qid;
    that.setData({
      qid: qid
    });
    var rcount = e.currentTarget.dataset.rcount;
    var ccount = e.currentTarget.dataset.ccount;
    //console.log(count);
    if (rcount == 0 && ccount == 0){
      app.tip({
        'title':'此問題尚未有回覆',
        'content':"搶先給予意見",
        'cb_confirm':function(){
          //console.log("sure");
          that.goToComment();
        },
        'cb_cancel':function(){
          console.log("cancel");
        }
      });
    }
    else{
      //console.log(qid);
      
      wx.navigateTo({
        url: "/pages/first/reply?qid=" + qid
      });
    }
    
    //console.log(this.data.qid);
  },


  bindShowCat() {
    this.setData({
      select: !this.data.select
    })
  },
  mySelect(e) {
    var that = this;
    var cat_id = e.currentTarget.dataset.cid;
    //console.log(e.currentTarget.dataset.cid);
    this.setData({
      select: false,
      cat_id: cat_id
    })
    this.getQuestionList(that.data.activeCategoryId, that.data.search_kw, cat_id);
  },


  goToComment(){
    var that = this;
    wx.navigateTo({
      url: "/pages/first/reply?qid=" + that.data.qid
    });
  },
  onPullDownRefresh() {
    this.getQuestionList();
  },
  toAsk: function() {
    wx.navigateTo({
      url: '/pages/question-ask/question-ask',
    });
  },

  setActiveId: function(e){
    var id = e.currentTarget.dataset.id;
    //console.log(id);
    this.setData({
      activeCategoryId: id,
    });

    //過濾問題
    //發送過濾請求
    this.getQuestionList(this.data.activeCategoryId, this.data.search_kw, this.data.cat_id);
  },

  getSearchInput: function(e){
    //console.log(e.detail.value);
    this.setData({search_kw:e.detail.value});
  },

  toSearch: function(e){
    this.getQuestionList(this.data.activeCategoryId, this.data.search_kw, this.data.cat_id)
  },


  getQuestionList: function (activeCategoryId=-1, search_kw="", cat_id=-1){
    var that = this;
    
    wx.request({
      url: app.buildUrl("/get-content"),
      method: "POST",
      data: {
        'active_cat_id': activeCategoryId,
        'action': "get_content",
        'search_kw':search_kw,
        'cat_id':cat_id
      },
      header: app.getRequestHeader(),
      success: function (res) {
        if (res.data.code == 200) {
          console.log(res);
          that.setData({
            qu: res.data.data[0],
            date: res.data.date,
            qid: ""+res.data.data[0]['id'],
            cat: res.data.cat[0],
            cat_id:res.data.cat_id
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