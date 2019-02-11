;
var user_login_ops = {
  init: function () {
    this.eventBind();
  },
  eventBind: function () {
    $('.login_wrap .do-login').click(function () {

        var btn_target = $(this);
        if (btn_target.hasClass("disable")){
            common_ops.alert("正在處理，請勿重複提交");
            return;
        }

        var login_name = $('#username').val();
        var login_pwd = $('#password').val();

        if (login_name == undefined || login_name.length < 1){
            common_ops.alert("請輸入正確的登錄用戶名");
            return;
        }

        if (login_pwd == undefined || login_pwd.length < 1){
            common_ops.alert("請輸入正確的密碼");
            return;
        }

        btn_target.addClass("disable");

        $.ajax({
            url:common_ops.buildUrl("/user/login"),
            type: 'POST',
            data: {'login_name':login_name, 'login_pwd':login_pwd},
            dataType: 'json',
            success:function (res) {
                btn_target.removeClass("disable");
                var callback = null;
                if (res.code == 200){
                    callback = function () {
                        window.location.href = common_ops.buildUrl("/");
                    }
                }
                common_ops.alert(res.msg, callback);
            }
        });
    });
  }
};


$(document).ready(function () {
   user_login_ops.init();
});