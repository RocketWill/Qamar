;
var comment_index_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });

        $(".remove").click(function () {
            that.ops("remove",$(this).attr("cid"));
        });

        $(".recover").click(function () {
            that.ops("recover",$(this).attr("cid"));
        });
    },

    ops: function (act, cid) {
        var callback = {
            'ok': function () {
                $.ajax({
                    url: common_ops.buildUrl("/comment/ops"),
                    dataType: 'json',
                    type: "POST",
                    data: {
                        "act": act,
                        "cid": cid,
                        "qid": $('input[name=qid]').val()
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
    comment_index_ops.init();
});