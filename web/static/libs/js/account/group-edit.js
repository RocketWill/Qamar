;
var user_edit_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".group_edit_wrap .save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var name_target = $('#group_name');
            var name = name_target.val();
            var des_target = $('#group_description');
            var des = des_target.val();
            var weight_target = $('#group_weight');
            var weight = weight_target.val();

            if (!name || name.length < 2){
                common_ops.tip("請輸入符合規範的姓名", name_target);
                return false;
            }

            if (parseInt(weight) < 1 || !weight || parseInt(weight)==undefined){
                common_ops.tip("請輸入符合規範的權重（不得小於 1）", weight_target);
                return false;
            }


            btn_target.addClass("disable");

            var data = {
                'name':name,
                'description':des,
                'weight':weight
            }

            $.ajax({
                url:common_ops.buildUrl('/account/group-edit'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/account/group-set");
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

