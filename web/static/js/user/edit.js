;
var edit_user_ops = {
    init:function () {
        this.bindEvents()
    },
    bindEvents:function () {
        $('.user_edit_wrap .save').click(function () {
            var btn_target =$(this);
            if (btn_target.hasClass("disabled")){
                common_ops.alert("正在处理，请勿重复提交~~");
                return;
            }

            var nickname_target = $('.user_edit_wrap input[name=nickname]');
            var nickname = nickname_target.val();

            var email_target = $('.user_edit_wrap input[name=email]');
            var email = email_target.val();

            if(nickname==undefined || nickname.length<1){
                common_ops.tip("请输入正确的昵称~~~",nickname_target)
            }

            if(email==undefined || email.length<1){
                common_ops.tip("请输入正确的昵称~~~",email_target)
            }
            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl('/user/edit'),
                type:'POST',
                data:{
                    nickname:nickname,
                    email:email
                },
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disabled");
                    var cb=null;
                    if(res.code == 200){
                        cb=function(){
                            window.location.href=window.location.href;
                        };

                    }
                    common_ops.alert(res.msg,cb)
                }
            })

        })
    }
};

$(document).ready(function () {
   edit_user_ops.init()
});