;
var user_edit_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".user_edit_wrap .save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var nickname_target = $('#nickname');
            var nickname = nickname_target.val();
            var email_target = $('#email');
            var email = email_target.val();

            if (!nickname || nickname.length < 2){
                common_ops.tip("請輸入符合規範的姓名", nickname_target);
                return false;
            }

            if (!email || email.length < 2){
                common_ops.tip("請輸入符合規範的郵箱", email_target)
                return false;
            }

            btn_target.addClass("disable");

            var data = {
                'nickname':nickname,
                'email':email
            }

            $.ajax({
                url:common_ops.buildUrl('/user/edit'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/user/edit");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });



        });
    }
};

$(document).ready(function () {
    user_edit_ops.init();
});

