;
var member_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $('.wrap_search .search').click(function () {
            $('.wrap_search').submit();
        });

        $('.remove').click(function () {
            that.ops('remove', $(this).attr('data'));
        });

        $('.recover').click(function () {
            that.ops('recover', $(this).attr('data'));
        });
    },
    ops: function (act, id) {
        var cb={
            'ok':function () {
                 $.ajax({
            url: common_ops.buildUrl('/member/ops'),
            type: 'POST',
            data: {
                id: id,
                act: act
            },
            dataType: 'json',
            success: function (res) {
                var cb = null;
                if (res.code == 200) {
                    cb = function () {
                        window.location.href = window.location.href;
                    }
                }
                common_ops.alert(res.msg, cb)
            }
        })
            },
            'cancel':null
        };
        common_ops.confirm((act == "remove"?"确认删除？":"确认恢复？"),cb)

    }
};

$(document).ready(function () {
    member_index_ops.init()
});