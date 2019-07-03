;
var reset_user_pwd = {
    init: function () {
        this.bindEvents();
    },
    bindEvents: function () {
        $('#save').click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert('请勿重复提交~~')
            }

            var old_password = $('#old_password').val();
            var new_password = $('#new_password').val();

            if (old_password == undefined || old_password.length < 6) {
                common_ops.alert("请输入正确的密码")
            }

            if (new_password == undefined || new_password.length < 6) {
                common_ops.alert("请输入正确的新密码")
            }

            if (old_password == new_password) {
                common_ops.alert("新旧密码不能相同~~")
            }

            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl('/user/reset-pwd'),
                type: 'POST',
                data: {
                    old_password: old_password,
                    new_password: new_password
                },
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    if (res.code == 200) {
                        common_ops.alert(res.msg)
                    }else{
                        common_ops.alert(res.msg)
                    }
                }
            })
        });

    }
};

$(document).ready(function () {
    reset_user_pwd.init()
});