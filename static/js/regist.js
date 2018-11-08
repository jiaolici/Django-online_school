// 切换验证码
$(function () {
    var imgcaptcha = $('.captcha');
    imgcaptcha.click(function () {
        imgcaptcha.attr('src', '/img_captcha'+"?random="+Math.random())
    })
});


$(function () {
    var send_sms = $('.sendcode')
    function send () {
        var telephone = $('#jsRegMobile').val();
        $.ajax({
            'url':'/api-list/send_sms/',
            'data':{
                'mobile': telephone,
            },
            "method":"post",
            'success':function (result) {
                var uuid = $('#uuid');
                uuid.attr('value',result['uuid']);
                console.log(uuid.val());
                var counter = 60;
                send_sms.unbind('click');
                var timer = setInterval(function () {
                    send_sms.val(counter);
                    counter--;
                    if(counter<=0){
                        clearInterval(timer);
                        send_sms.val('发送短信验证码');
                        send_sms.click(send)
                    }
                },1000)
            }
        })
    }
    send_sms.click(send)
})