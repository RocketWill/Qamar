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
        reply_ops.delete_file();
    }
};
var reply_ops = {
    init: function () {
        this.eventBind();
        this.initEditor();
        this.delete_file();
    },
    eventBind: function () {
        var that = this;

        $('.replay-wrap select[name=cat_id]').select2({
            language:'zh-CN',
            width:'100%'
        });

        $('.replay-wrap input[name=tags]').tagsInput({
            width:'auto',
            height:40,
        });

        $('#upload-file').change(function () {
            console.log("work");
            $('.upload_file_wrap').submit();
            console.log("work2");
        });



        $(".replay-wrap .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var title_target = $('#title');
            var title = title_target.val();

            // var content_target = $('#content');
            // var content = content_target.val();


            //alert(cat_id);

            var content = $.trim(that.ue.getContent());

            var tags_target = $("input[name=tags]");
            var tags = $.trim(tags_target.val())

            // if (parseInt(cat_id) < 1){
            //     common_ops.tip("請選擇問題分類",cat_id_target);
            //     return false;
            // }

            if (!content || content.length < 10) {
                common_ops.alert("請輸入至少10字的回覆");
                return false;
            }

            console.log($(".del_file").attr("data"));


            btn_target.addClass("disable");

            var data = {
                'title': title,
                'content': content,
                'tags':tags,
                'file':$(".del_file").attr("data"),
                'aid': $("#aid").val(),
                'qid': $("#qid").val(),
                'uid': $("#uid").val(),
            }

            $.ajax({
                url: common_ops.buildUrl('/question/reply'),
                type: "POST",
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/question/reply");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });

    },

    ops: function (act, uid) {
        var callback = {
            'ok': function () {
                $.ajax({
                    url: common_ops.buildUrl("/member/ops"),
                    dataType: 'json',
                    type: "POST",
                    data: {
                        "act": act,
                        "id": uid
                    },
                    success: function (res) {
                        var callback = null;
                        if (res.code == 200) {
                            callback = function () {
                                window.location.href = window.location.href;
                            }
                        }

                        common_ops.alert(res.msg, callback);
                    }
                });
            },

            'cancel': null
        };
        common_ops.confirm((act == "remove" ? '確定刪除？' : "確定恢復？"), callback);
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
    delete_file:function () {
       $(".del_file").unbind().click(function () {
           $(this).parent().remove();
       });
    }
};

$(document).ready(function () {
    reply_ops.init();
});