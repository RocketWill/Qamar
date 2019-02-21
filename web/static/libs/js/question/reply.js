;
var reply_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        $(".replay-wrap .save").click(function () {
           var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var title_target = $('#title');
            var title = title_target.val();

            var content_target = $('#content');
            var content = content_target.val();

            if (!content || content.length < 10){
                common_ops.tip("請輸入至少10字的回覆", content_target);
                return false;
            }


            btn_target.addClass("disable");

            var data = {
                'title':title,
                'content':content,
                'uid':$("#uid").val(),
                'qid':$("#qid").val(),
            }

            $.ajax({
                url:common_ops.buildUrl('/question/reply'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
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
                    success:function (res) {
                        var callback = null;
                        if (res.code == 200){
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
        common_ops.confirm((act == "remove"? '確定刪除？' : "確定恢復？"), callback);
    }
};

$(document).ready(function () {
    reply_ops.init();
});