;
var user_reset_pwd_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".user_reset_pwd_wrap .save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var origin_pwd_target = $('#original_pwd');
            var origin_pwd = origin_pwd_target.val();
            var new_pwd_target = $('#new_pwd');
            var new_pwd = new_pwd_target.val();
            var new_pwd_auth_target = $('#new_pwd_auth');
            var new_pwd_auth = new_pwd_auth_target.val();

            if (!origin_pwd || origin_pwd < 1){
                common_ops.tip("請輸入符合規範的原密碼", origin_pwd_target);
                return;
            }

            if (!new_pwd || new_pwd.length < 6 || !new_pwd_auth || new_pwd_auth.length < 6 || new_pwd !== new_pwd_auth){
                common_ops.tip("請輸入符合規範新密碼 (須大於6位)", new_pwd_auth_target);
                return;
            }

            btn_target.addClass("disable");

            var data = {
                'old-pwd':origin_pwd,
                'new-pwd':new_pwd
            }

            $.ajax({
                url:common_ops.buildUrl('/user/reset-pwd'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/user/reset-pwd");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });



        });
    }
};

$(document).ready(function () {
    user_reset_pwd_ops.init();
});

