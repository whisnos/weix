;
var account_set_ops = {
   init:function () {
       this.bindEvents();
   },
   bindEvents:function () {
        $('.wrap_account_set .save').click(function () {
            var btn_target=$(this);
            if (btn_target.hasClass('disabled')){
                common_ops.alert("请勿重复提交~~");
                return;
            }

            var nickname_target=$('.wrap_account_set input[name=nickname]');
            var nickname= nickname_target.val();

            var mobile_target=$('.wrap_account_set input[name=mobile]');
            var mobile=mobile_target.val();

            var email_target=$('.wrap_account_set input[name=email]');
            var email=email_target.val();

            var login_name_target=$('.wrap_account_set input[name=login_name]');
            var login_name=login_name_target.val();

            var login_pwd_target=$('.wrap_account_set input[name=login_pwd]');
            var login_pwd=login_pwd_target.val();

            if (nickname == undefined || nickname.length<1){
                common_ops.tip("请输入正确的用户名~~",nickname_target)
            }

            if (mobile == undefined || mobile.length != 11){
                common_ops.tip("请输入正确的手机号~~",mobile_target)
            }

            if (email == undefined || email.length<4){
                common_ops.tip("请输入正确的邮箱~~",email_target)
            }

            if (login_name == undefined || login_name.length<1){
                common_ops.tip("请输入正确的登录名~~",login_name_target)
            }

            if (login_pwd == undefined || login_pwd<6){
                common_ops.tip("请输入正确的密码~~",login_pwd_target)
            }

            $.ajax({
                url:common_ops.buildUrl('/account/set'),
                type:'POST',
                data:{
                    nickname:nickname,
                    mobile:mobile,
                    email:email,
                    login_name:login_name,
                    login_pwd:login_pwd,
                    id:$('.wrap_account_set input[name=id]').val()
                },
                dataType:'json',
                success:function (res) {
                    if (res.code==200){
                        common_ops.alert(res.msg)
                    }
                }
            })
        })
   }
};

$(document).ready(function () {
    account_set_ops.init();
});