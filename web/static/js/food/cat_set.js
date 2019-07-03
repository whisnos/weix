;
var member_catset_ops = {
   init:function () {
       this.bindEvents();
   },
   bindEvents:function () {
        $('.wrap_cat_set .save').click(function () {
            var btn_target=$(this);
            if (btn_target.hasClass('disabled')){
                common_ops.alert("请勿重复提交~~");
                return;
            }

            var name_target=$('.wrap_cat_set input[name=name]');
            var name= name_target.val();

            var weight_target=$('.wrap_cat_set input[name=weight]');
            var weight=weight_target.val();

            if (name == undefined || name.length<1){
                common_ops.tip("请输入正确的分类名~~",name_target);
                return false;
            }

            if (weight == undefined || parseInt(weight) < 1){
                common_ops.tip("请输入正确的权重,并且至少大于1~~",weight_target);
                return false;
            }

            $.ajax({
                url:common_ops.buildUrl('/food/cat-set'),
                type:'POST',
                data:{
                    name:name,
                    weight:weight,
                    id:$('.wrap_cat_set input[name=id]').val()
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
    member_catset_ops.init();
});