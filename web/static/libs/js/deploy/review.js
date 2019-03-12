;
var deploy_review_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        $("select[name^=review-]").change(function () {
            //console.log($("select[name^=set_cat_id-]").val());
            //console.log("good")
            //$(".wrap_search").submit();
            console.log($(this).val());
            var set_review = $(this).val();
            $.ajax({
                url: common_ops.buildUrl('/deploy/review'),
                type: "POST",
                data: {set_review: set_review},
                dataType: 'json',
                success: function (res) {
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });
    },


};

$(document).ready(function () {
    deploy_review_ops.init();
});