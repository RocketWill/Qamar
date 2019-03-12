;
var account_group_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        $(".wrap_search select[name=status]").change(function () {
            $(".wrap_search").submit();
        });

        $(".remove").click(function () {
            that.ops("remove",$(this).attr("user_group_id"));
        });

        $(".recover").click(function () {
            that.ops("recover",$(this).attr("user_group_id"));
        });
    },

    ops: function (act, grp_id) {
        var callback = {
            'ok': function () {
                $.ajax({
                    url: common_ops.buildUrl("/account/ops"),
                    dataType: 'json',
                    type: "POST",
                    data: {
                        "act": act,
                        "grp_id": grp_id,
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
        common_ops.confirm((act == "remove"? '確定刪除？刪除後用戶組內的所有帳戶將同時被停權，同時相關問題回答也會標記為無效' : "確定恢復？"), callback);
    }
};

$(document).ready(function () {
    account_group_set_ops.init();
});