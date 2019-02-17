;
var mail_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        $(".mail_wrap .save").click(function () {
            var email = $("#email").val();
            console.log(email);

            $.ajax({
                url:common_ops.buildUrl('/mail/validation'),
                type:"POST",
                data:{'email':email},
                dataType:'json',
                success:function (res) {

                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            //window.location.href = window.location.href;
                            $("#result").html(res.msg);
                        }
                    }
                    common_ops.alert(res.msg, callback);
                    $("#result").html(res.msg);
                    $("#result2").html(res.token);
                }
            });
        });



    },


};

$(document).ready(function () {
    mail_ops.init();
});