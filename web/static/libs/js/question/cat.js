;
var question_cat_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        $(".wrap_search select[name=status]").change(function () {
            $(".wrap_search").submit();
        });

        $(".remove").click(function () {
            that.ops("remove",$(this).attr("cat_id"));
        });

        $(".recover").click(function () {
            that.ops("recover",$(this).attr("cat_id"));
        });
    },

    ops: function (act, cat_id) {
        var callback = {
            'ok': function () {
                $.ajax({
                    url: common_ops.buildUrl("/question/cat-ops"),
                    dataType: 'json',
                    type: "POST",
                    data: {
                        "act": act,
                        "cat_id": cat_id
                    },
                    success:function (res) {
                        var callback = null;
                        if (res.code == 200){
                            callback = function () {
                                window.location.href = window.location.href;
                            }
                        }

                        common_ops.alert(res.msg, callback);
                    }
                });
            },

            'cancel': null
        };
        common_ops.confirm((act == "remove"? '確定刪除？' : "確定恢復？"), callback);
    }
};

$(document).ready(function () {
    question_cat_ops.init();
});