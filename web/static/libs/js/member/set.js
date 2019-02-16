;
var member_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {

        var email_check = 0

        $("#email_valid").on("click", function () {
            var item = $("#email_valid")
            if(item.attr('checked')){
                item.attr('checked', false);
                email_check = 0
                //console.log(email_check);
            }else{
                item.attr('checked', true);
                email_check = 1
                //console.log(email_check);
            }
        });

        $(".member_set_wrap .save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var nickname_target = $('#nickname');
            var nickname = nickname_target.val();

            var email_valid = $('#email_valid');

            if (!nickname || nickname.length < 2){
                common_ops.tip("請輸入符合規範的姓名", nickname_target);
                return false;
            }





            btn_target.addClass("disable");

            var data = {
                'nickname':nickname,
                'email_check':email_check,
                'id':$("#id").val()
            }

            $.ajax({
                url:common_ops.buildUrl('/member/set'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/member/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });



        });
    }
};

$(document).ready(function () {
    member_set_ops.init();
});

