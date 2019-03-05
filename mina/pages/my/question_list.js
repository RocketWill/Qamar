var app = getApp();
Page({
  data: {
    statusType: ["全部", "官方解答", "待解答", "同學意見"],
    status: ["0", "1", "2", "3"],
    currentType: 0,
    tabClass: ["", "", "", "", "", ""]
  },
  statusTap: function(e) {
    console.log(e.currentTarget.dataset.index);
    var curType = e.currentTarget.dataset.index;
    this.data.currentType = curType;
    this.setData({
      currentType: curType
    });
    this.onShow();
  },
  
  questionDetail: function(e) {
    var qid = "" + e.currentTarget.dataset.qid;
    var count = e.currentTarget.dataset.count;
    //console.log(count);
    if (count == 0) {
      app.tip({
        'content': "此問題尚未有回覆"
      });
      return;
    } else {
      //console.log(qid);
      wx.navigateTo({
        url: "/pages/first/reply?qid=" + qid
      });
    }

    //console.log(this.data.qid);
  },
  questionEdit: function(e){
    var qid = "" + e.currentTarget.dataset.qid;
      //console.log(qid);
      wx.navigateTo({
        url: "/pages/question-ask/question-ask?qid=" + qid
      });
  },
  onLoad: function(options) {
    // 生命周期函数--监听页面加载

  },
  onReady: function() {
    // 生命周期函数--监听页面初次渲染完
  },
  onShow: function(currentType = 0) {
    var that = this;

    wx.request({
      url: app.buildUrl("/get-my-question"),
      method: "POST",
      data: {
        "token": app.getCache("token"),
        'current_type': that.data.currentType
      },
      header: app.getRequestHeader(),
      success: function(res) {
        console.log(res);
        if (res.data.code == 200) {
          that.setData({
            question_list: res.data.question_list[0]
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
  onHide: function() {
    // 生命周期函数--监听页面隐藏

  },
  onUnload: function() {
    // 生命周期函数--监听页面卸载

  },
  onPullDownRefresh: function() {
    // 页面相关事件处理函数--监听用户下拉动作

  },
  onReachBottom: function() {
    // 页面上拉触底事件的处理函数

  }
})