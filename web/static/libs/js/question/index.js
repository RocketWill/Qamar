;
var question_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {

        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });

        $(".remove").click(function () {
            that.ops("remove", $(this).attr("uid"));
        });

        $(".recover").click(function () {
            that.ops("recover", $(this).attr("uid"));
        });




        btn_target.addClass("disable");

        var data = {
            'nickname': nickname,
            'email_check': email_check,
            'id': $("#id").val()
        }

        $.ajax({
            url: common_ops.buildUrl('/member/set'),
            type: "POST",
            data: data,
            dataType: 'json',
            success: function (res) {
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

    },


};

$(document).ready(function () {
    question_index_ops.init();
});