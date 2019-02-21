;
var edit_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        $(".edit-wrap .save").click(function () {
           var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var content_target = $('#content');
            var content = content_target.val();

            if (!content || content.length < 10){
                common_ops.tip("請輸入至少10字的回覆", content_target);
                return false;
            }


            btn_target.addClass("disable");

            var data = {
                'content':content,
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

};

$(document).ready(function () {
    edit_ops.init();
});