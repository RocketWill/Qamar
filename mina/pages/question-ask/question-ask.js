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
    images: [],
    anony: false,
    randomStr: app.randomString(false,12),
  },

  onLoad(options) {
    var that = this;
    $init(this)
    if (options.qid){
      that.setData({qid:options.qid});
      wx.request({
        url: app.buildUrl("/get-question"),
        method: "POST",
        data: {
          "qid": options.qid,
          'action': "edit"
        },
        header: app.getRequestHeader(),
        success: function (res) {
          console.log(res);
          for(var i=0;i<res.data.file.length;i++){
            res.data.file[i] = app.buildImageUrl(res.data.file[i]);
          }
          if (res.data.code == 200) {
            that.setData({
              question : res.data.question,
              titleCount: res.data.question['title'].length,
              contentCount: res.data.question['content'].length,
              anony: res.data.question['anony'] == '匿名' ? true : false,
              pre_images : res.data.file,
              title: res.data.question['title'],
              content:res.data.question['content']
            });
            return;
          }
          if (res.data.code == -1) {
            app.alert({
              'content': res.data.msg
            });
            return;
          }
        }
      });
    }
    
  },

  onShow(){
    this.setData({
      randomStr: app.randomString(false, 12)
    });
  },

  anonymChange: function(e) {
   // console.log(`Switch样式点击后是否选中：`, e.detail.value)
    if (e.detail.value == false){
      this.setData({
        anony: false,
      });
      console.log(this.data.anony);
    }else{
      this.setData({
        anony: true,
      });
      console.log(this.data.anony);
    }
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

  clearContent: function() {
    this.setData({
      title: '',
      titleCount: 0,
    });
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

  handlePreImagePreview(e) {
    const idx = e.target.dataset.preidx
    const images = this.data.pre_images

    wx.previewImage({
      current: images[idx],
      urls: images,
    })
  },

  cancelEdit: function() {
    var that = this;
    const title = this.data.title
    const content = this.data.content
    if (title.length<1 && content.length<1) {
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

  goToEmailVerify:function(){
    wx.navigateTo({
      url: "/pages/email/index"
    });
  },

  sureAsk: function() {
    var that = this;
  
    if (this.data.titleCount < 10) {
      app.alert({
        'content': "問題標題字數不能少於10字"
      });
      return;
    }

    if (this.data.contentCount < 20) {
      app.alert({
        'content': "問題內容字數不能少於20字"
      });
      return;
    }
    wx.showModal({
      title: '提示',
      content: !this.data.pre_images? '確定發問？':'確定修改',
      success(res) {
        if (res.confirm) {
          that.submitForm();
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },

  submitForm(e) {
    console.log("works");
    var that = this;
    const title = this.data.title
    const content = this.data.content
    var anony = this.data.anony
    const randomStr = this.data.randomStr

    if (title && content) {
      var that = this;
      const arr = []
      console.log(this.data.images);

      //将选择的图片组成一个Promise数组，准备进行并行上传
      for (let path of this.data.images) {
        arr.push(wxUploadFile({
          url: app.buildUrl("/get-question"),
          filePath: path,
          name: 'post-question',
          formData: {
            'title': title,
            'content': content,
            'random_str': randomStr,
            'token': app.getCache('token'),
            'action': 'create',
            'qid': that.data.qid?that.data.qid:'',
            'action': that.data.qid? "post-edit" : ''
          }
        }))
      }

      console.log(arr);

      wx.showLoading({
        title: '正在创建...',
        mask: true
      })

      if (arr.length < 1) {
        wx.request({
          url: app.buildUrl("/get-question"),
          method: "POST",
          data: {
            'title': title,
            'content': content,
            'anony':anony,
            'random_str': randomStr,
            'token': app.getCache('token'),
            'qid': that.data.qid?that.data.qid:'',
            'action': that.data.qid? "post-edit" : ''
          },
          header: app.getRequestHeader(),
          success: function(res) {

            //console.log(res);
            if (res.data.code == 200) {
              wx.hideLoading();
              app.alert({
                'content': '提交成功',
                'cb_confirm': function() {
                  that.goToIndex();
                }
              });
            }

            if (res.data.code == 300){
              wx.hideLoading();
              wx.showModal({
                title: 'OOPS！請先驗證郵箱',
                content: res.data.msg,
                success(res) {
                  if (res.confirm) {
                    that.goToEmailVerify();
                  } else if (res.cancel) {
                    that.cancelEdit()
                  }
                }
              })
            }

            if (res.data.code==-1){
              wx.hideLoading();
              app.alert({
                'content': res.data.msg
              });
              return;
            }

          }
        });
        return;
      }

      // 开始并行上传图片
      Promise.all(arr).then(res => {
        var result = JSON.parse(res[0]['data']);
        console.log(result); 
        // 上传成功，获取这些图片在服务器上的地址，组成一个数组
        if (result.code == 200) {
          //wx.hideLoading();
           
          app.alert({
            'content': '提交成功',
            'cb_confirm': function () {
              that.goToIndex();
            }
          });
        }
        if (result.code == 300) {
          //wx.hideLoading();
          wx.showModal({
            title: 'OOPS！請先驗證郵箱',
            content: result.msg,
            success(res) {
              if (res.confirm) {
                that.goToEmailVerify();
              } else if (res.cancel) {
                that.cancelEdit()
              }
            }
          })
        }
        console.log(res);
      }).catch(err => {
        console.log(">>>> upload images error:", err)
        app.alert({
          'content': "Oh no！似乎有什麼出錯了，請稍後再試",
          'cb_confirm': function () {
            that.goToIndex();
          }
        });
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