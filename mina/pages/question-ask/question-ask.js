import {
  promisify
} from '../../utils/promise.util'
import {
  $init,
  $digest
} from '../../utils/common.util'
//import { createQuestion } from '../../services/question.service'
//import config from '../../config'

var app = getApp();
const wxUploadFile = promisify(wx.uploadFile)

Page({

  data: {
    titleCount: 0,
    contentCount: 0,
    title: '',
    content: '',
    images: []
  },

  onLoad(options) {
    $init(this)
  },

  createQuestion: function(data) {
    return exec({
      url: app.buildUrl("/get-question"),
      method: 'post',
      data
    })
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

  chooseImage(e) {
    var that = this;
    wx.chooseImage({
      count: 3,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],

      success: function(res) {
        console.log(res);
        const images = that.data.images.concat(res.tempFilePaths);
        that.data.images = images.length <= 3 ? images : images.slice(0, 3);
        $digest(that);
      }
    })
  },

  removeImage(e) {
    const idx = e.target.dataset.idx
    this.data.images.splice(idx, 1)
    $digest(this)
  },

  goToIndex: function () {
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

  submitForm(e) {
    var that = this;
    const title = this.data.title
    const content = this.data.content

    if(title == undefined || title == null || title.length< 10){
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

    if (title && content) {
      var that = this;
      const arr = []
      console.log(this.data.images);

      //将选择的图片组成一个Promise数组，准备进行并行上传
      for (let path of this.data.images) {
        arr.push(wxUploadFile({
          url: app.buildUrl("/get-question"),
          filePath: path,
          name: 'shit',
          formData: {
            'title':title,
            'content':content,
            'token':app.getCache('token'),
            'action':'create'
          }
        }))
      }

      console.log(arr);

      wx.showLoading({
        title: '正在创建...',
        mask: true
      })

      if (arr.length < 1){
        wx.request({
          url: app.buildUrl("/get-question"),
          method: "POST",
          data: {
            'title': title,
            'content': content,
            'token': app.getCache('token'),
             },
          header: app.getRequestHeader(),
          success: function (res) {
            
            //console.log(res);
            if (res.data.code == 200) {
              wx.hideLoading();
              app.alert({
                'content':'提交成功',
                'cb_confirm': function () {
                  that.goToIndex();
                }
              });
            }
            
          }
        });
        return;
      }

      // 开始并行上传图片
      Promise.all(arr).then(res => {
        // 上传成功，获取这些图片在服务器上的地址，组成一个数组
        console.log(res.map(item => JSON.parse(item.data).url));
        return res.map(item => JSON.parse(item.data).url)
      }).catch(err => {
        console.log(">>>> upload images error:", err)
      }).then(urls => {
        // 调用保存问题的后端接口
        // return that.createQuestion({
        //   title: title,
        //   content: content,
        //   images: urls
        // })
        wx.hideLoading()
      })
      // .then(res => {
      //   // 保存问题成功，返回上一页（通常是一个问题列表页）
      //   const pages = getCurrentPages();
      //   const currPage = pages[pages.length - 1];
      //   const prevPage = pages[pages.length - 2];

      //   // 将新创建的问题，添加到前一页（问题列表页）第一行
      //   prevPage.data.questions.unshift(res)
      //   $digest(prevPage)

      //   wx.navigateBack()
      // }).catch(err => {
      //   console.log(">>>> create question error:", err)
      // }).then(() => {
      //   wx.hideLoading()
      // })
    }
  },

  uploadimg: function() { //这里触发图片上传的方法
    var pics = this.data.images;
    app.uploadimg({
      url: app.buildUrl("/get-question"),
      path: pics //这里是选取的图片的地址数组
    });
  },

})