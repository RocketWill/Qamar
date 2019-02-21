;
var question_allreply_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });
    },


};

$(document).ready(function () {
    question_allreply_ops.init();
});