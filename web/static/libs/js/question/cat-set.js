;
var food_cat_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".food_cat_set_wrap .save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                common_ops.alert("正在處理，請勿重複提交");
                return;
            }

            var name_target = $('#cat_name');
            var cat_name = name_target.val();

            var weight_target = $('#weight');
            var weight = weight_target.val();

            if (!cat_name || cat_name.length < 2){
                common_ops.tip("請輸入不少於2個字符的分類名稱", name_target);
                return false;
            }

            console.log(parseFloat(weight).toString());

            if (parseFloat(weight).toString() == "NaN"){
                common_ops.tip("請輸入正整數", weight_target)
                return false;
            }



            btn_target.addClass("disable");

            var data = {
                'cat_name':cat_name,
                'cat_weight':weight,
                'cat_id':$("#cat_id").val()
            }

            $.ajax({
                url:common_ops.buildUrl('/question/cat-set'),
                type:"POST",
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/question/cat");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });



        });
    }
};

$(document).ready(function () {
   food_cat_set_ops.init();
});

