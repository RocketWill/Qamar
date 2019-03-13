;
var account_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".account_set_wrap .save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var nickname_target = $('#nickname');
            var nickname = nickname_target.val();

            var email_target = $('#email');
            var email = email_target.val();

            var mobile_target = $('#mobile');
            var mobile = mobile_target.val();

            var login_name_target = $('#login_name');
            var login_name = login_name_target.val();

            var login_pwd_target = $('#login_pwd');
            var login_pwd = login_pwd_target.val();

            if (!nickname || nickname.length < 2){
                common_ops.tip("請輸入符合規範的姓名", nickname_target);
                return false;
            }

            if (!email || email.length < 2){
                common_ops.tip("請輸入符合規範的郵箱", email_target)
                return false;
            }

            if (!mobile || mobile.length < 2){
                common_ops.tip("請輸入符合規範的手機號", mobile__target)
                return false;
            }

            if (!login_name || login_name.length < 2){
                common_ops.tip("請輸入符合規範的登錄名稱", login_name_target)
                return false;
            }

            if (!login_pwd || login_pwd.length < 6){
                common_ops.tip("請輸入符合規範的密碼", login_pwd_target)
                return false;
            }



            btn_target.addClass("disable");

            var data = {
                'nickname':nickname,
                'email':email,
                'mobile':mobile,
                'login_name':login_name,
                'login_pwd':login_pwd,
                'id':$("#uid").val(),
                'user_group_id': $("#user_group_id").val(),
            }

            $.ajax({
                url:common_ops.buildUrl('/account/set'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.replace(document.referrer);
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });



        });
    }
};

$(document).ready(function () {
    account_set_ops.init();
});

