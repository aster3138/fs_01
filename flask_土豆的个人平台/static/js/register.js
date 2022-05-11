// 绑定验证码的点击事件
function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click", function (event){
        let $this =$(this);  //$(this)代指$("#captcha-btn")
        let email = $("input[name='email']").val();   //val()代表获取输入框中的值
                                                    //z这里传入的字符串代表获取某个按钮,根据id获取，则：先写 # ，再写名称：captcha-btn
                                                     //on，代表出现什么事，执行什么代码，出现点击事件，执行函数function（event）
        if(!email){
            alert("请输入邮箱！");
        }
        // 通过js请求发送网络请求
        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data: {
                "email":email
            },
            success: function (res){   //res代表user.get_captcha返回的参数
                let code = res['code'];
                if (code === 200){
                    // 取消点击事件
                    $this.off("click")
                    // 开始倒计时
                    let countDown = 60;
                    // setInterval定时器，可以指定每隔多少时间，执行某件事，每隔1秒钟，更新一下按钮上的文字
                    let timer = setInterval(function (){
                        countDown -= 1;
                        if(countDown > 0){
                            $this.text(countDown+"秒后重新发送！");  // 修改$this里的值，也就是 获取验证码 这个按钮里的文字
                        }else{
                            $this.text("获取验证码");
                            // 重新执行下这个函数，重新绑定点击事件
                            bindCaptchaBtnClick();
                            // 如果不需要倒计时了，那么就要记得清除倒计时，否则会一直执行下去
                            clearInterval(timer)  //清除定时器
                        }
                    },1000)
                    alert("验证码发送成功！");
                }else{
                    alert(res['message']);
                }
            }
            })
    });

}






//$()这里传入的函数里面的代码，只会在（浏览器页面）文档所有元素加载完成之后执行
$(function (){
    bindCaptchaBtnClick();
})

