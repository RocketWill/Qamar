import {
  promisify
} from '../../utils/promise.util'
import {
  $init,
  $digest
} from '../../utils/common.util'
//import { createQuestion } from '../../services/question.service'
//import config from '../../config'
var WxParse = require('../../wxParse/wxParse.js');
var utils = require('../../utils/util.js');
var app = getApp();
const wxUploadFile = promisify(wx.uploadFile)

Page({

  data: {
    titleCount: 0,
    contentCount: 0,
    title: '',
    content: '',
    images: [],
    anony: false,
    qid: "",
    randomStr: app.randomString(false, 12),
    reply: [{
      'title': "default",
      'content': 'default'
    }],
    listArr:""
  },

  onLoad(options) {
    $init(this);
    this.setData({
      qid: options.qid,
    });
    this.getReply();
  },

  onShow() {
    this.setData({
      randomStr: app.randomString(false, 12)
    });
  },


  handleTitleInput(e) {
    const value = e.detail.value
    this.data.title = value
    this.data.titleCount = value.length
    $digest(this)
  },

  handleContentInput(e) {
    const value = e.detail.value
    this.data.content = value
    this.data.contentCount = value.length
    $digest(this)
  },

  goToIndex: function() {
    wx.switchTab({
      url: "/pages/first/index"
    });
  },

  handleImagePreview(e) {
    const idx = e.target.dataset.idx
    const images = this.data.images

    wx.previewImage({
      current: images[idx],
      urls: images,
    })
  },

  cancelEdit: function() {
    var that = this;
    const title = this.data.title
    const content = this.data.content
    if (title.length < 1 && content.length < 1) {
      this.goToIndex();
    } else {
      wx.showModal({
        title: '提示',
        content: '確定放棄編輯？',
        success(res) {
          if (res.confirm) {
            that.goToIndex();
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    }

  },

  goToEmailVerify: function() {
    wx.navigateTo({
      url: "/pages/email/index"
    });
  },

  sureAsk: function() {
    var that = this;
    const title = this.data.title
    const content = this.data.content
    if (title == undefined || title == null || title.length < 10) {
      app.alert({
        'content': "問題標題字數不能少於10字"
      });
      return;
    }

    if (content == undefined || content == null || content.length < 10) {
      app.alert({
        'content': "問題內容字數不能少於20字"
      });
      return;
    }
    wx.showModal({
      title: '提示',
      content: '確定發問？',
      success(res) {
        if (res.confirm) {
          that.submitForm();
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  
  
previewImg:function(e){
  console.log(e.currentTarget.dataset.src);
  var img = e.currentTarget.dataset.src;
  // var imgArr = this.data.imgArr;
  wx.previewImage({
    current: app.buildImageUrl(img),     //当前图片地址
    urls: [app.buildImageUrl(img)],               //所有要预览的图片的地址集合 数组形式
    success: function(res) {},
    fail: function(res) {},
    complete: function(res) {},
  })
},

  getReply: function() {
    var that = this;
    wx.request({
      url: app.buildUrl("/get-reply"),
      method: "POST",
      data: {
        qid: this.data.qid
      },
      header: app.getRequestHeader(),
      success: function(res) {
        //console.log(res);
        if (res.data.code != 200) {

        }
        that.setData({
          reply: res.data.data_file[0]
          
        });
        console.log(res.data.data_file[0].length);

        //解析html
        let listRes = res.data.data_file[0]; //要解析的数据
        for (let i = 0; i < listRes.length; i++) {
          console.log(listRes[i]['reply'].content);
          WxParse.wxParse('topic' + i, 'html', listRes[i]['reply'].content, that);
          if (i === listRes.length - 1) {
            WxParse.wxParseTemArray("listArr", 'topic', listRes.length, that)
          }
        }

        let list = that.data.listArr;
        for (let i = 0; i < listRes.length; i++) {
          list[i]['title'] = listRes[i]['reply']['title'];
        }
        list.map((item, index, arr) => {
          arr[index][0].id = listRes[index]['reply']['id'];
          arr[index][0].title = listRes[index]['reply']['title'];
          arr[index][0].aid = listRes[index]['reply']['aid'];
          arr[index][0].cat_id = listRes[index]['reply']['cat_id'];
          arr[index][0].created_time = listRes[index]['reply']['created_time'];

          arr[index][0].nickname = listRes[index]['reply']['nickname'];
          arr[index][0].qid = listRes[index]['reply']['qid'];
          arr[index][0].tags = listRes[index]['reply']['tags'];
          arr[index][0].uid = listRes[index]['reply']['uid'];
          arr[index][0].updated_time = listRes[index]['reply']['updated_time'];
          arr[index][0].file_key = listRes[index]['image']['file_key'];
        });

        console.log(list);
        that.setData({
          list: list
        })
        

        console.log(res);
        //that.goToIndex();


      }

    });
  }


})