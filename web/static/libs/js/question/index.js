;
var question_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_search select[name=cat_id]").change(function () {
            //console.log("cat id");
            $(".wrap_search").submit();
        });

        $('select[name^=set_cat_id-]').select2({
            language: 'zh-CN',
            width: '100%'
        });

        $('select[name^=set_user_group-]').select2({
            language: 'zh-CN',
            width: '100%'
        });

        $("select[name^=set_cat_id-]").change(function () {
            //console.log($("select[name^=set_cat_id-]").val());
            //console.log("good")
            //$(".wrap_search").submit();
            var set_cat = $(this).val();
            $.ajax({
                url: common_ops.buildUrl('/question/index'),
                type: "POST",
                data: {set_cat: set_cat},
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

        $("select[name^=set_user_group-]").change(function () {
            //console.log($(this).val());
            var set_user_group = $(this).val();
             $.ajax({
                url: common_ops.buildUrl('/question/index'),
                type: "POST",
                data: {set_user_group: set_user_group},
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


        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });


    },


};

$(document).ready(function () {
    question_index_ops.init();
});