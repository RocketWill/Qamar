;
var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img style="width: 150px; margin-bottom: 20px;" src="' + common_ops.buildFileUrl(file_key) + '"/>'
            + '<span class="fa fa-times-circle del del_file" data="' + file_key + '"></span>';

        if ($(".show-upload-file-wrap .file-each").size() > 0) {
            $(".show-upload-file-wrap .file-each").html(html);
        } else {
            $(".show-upload-file-wrap").append('<span "width: 150px; margin-bottom: 100px;"  class="file-each">' + html + '</span>');
        }
        edit_ops.delete_file();
    }
};
var edit_ops = {
    init:function () {
        this.eventBind();
        this.initEditor();
        this.delete_file();
        this.setUeditorContent();
    },
    eventBind:function () {
        var that = this;

        $('select[name=cat_id]').select2({
            language: 'zh-CN',
            width: '100%'
        });

        $('input[name=tags]').tagsInput({
            width: 'auto',
            height: 40,
        });

        $('#upload-file').change(function () {
            console.log("work");
            $('.upload_file_wrap').submit();
            console.log("work2");
        });

        $(".edit-wrap .save").click(function () {
           var btn_target = $(this);



            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            //var content_target = $('#content');
            var content = $.trim(that.ue.getContent());
            var tags_target = $("input[name=tags]");
            var tags = $.trim(tags_target.val())

            if (!content || content.length < 10){
                common_ops.tip("請輸入至少10字的回覆", content_target);
                return false;
            }


            btn_target.addClass("disable");

            var data = {
                'content':content,
                'tags' : tags,
                'file':$(".del_file").attr("data"),
                'aid':$("#aid").val(),
                'qid':$("#qid").val(),
                'rid':$("#rid").val(),
            }

            $.ajax({
                url:common_ops.buildUrl('/question/edit'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/question/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });

    },
    initEditor: function () {
        var that = this;
        that.ue = UE.getEditor('content', {
            toolbars: [['undo', 'redo', '|', 'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|', 'rowspacingtop', 'rowspacingbottom', 'lineheight'], ['customstyle', 'paragraph', 'fontfamily', 'fontsize', '|', 'directionalityltr', 'directionalityrtl', 'indent', '|', 'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|', 'link', 'unlink'], ['imagenone', 'imageleft', 'imageright', 'imagecenter', '|', 'insertimage', 'insertvideo', '|', 'horizontal', 'spechars', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols']],
            enableAutoSave: true,
            saveInterval: 60000,
            elementPathEnabled: false,
            zIndex: 4,
            serverUrl: '/upload/ueditor'
        });
    },

    //set ueditor content
    setUeditorContent: function(){
        var that = this;
        var text = $("#content-invis").val();
        setTimeout(function () {
            that.ue.setContent(text, false);
        },666);
    },

    delete_file:function () {
       $(".del_file").unbind().click(function () {
           $(this).parent().remove();
       });
    }
};

$(document).ready(function () {
    edit_ops.init();
});