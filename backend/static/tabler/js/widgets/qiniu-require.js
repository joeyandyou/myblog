require.config({
    paths: {
        'qiniu': '/static/tabler/js/widgets/qiniu',
    }
})
require(['jquery', 'qiniu'], function($){
    $(function(){
        $('.qiniu input').attr('type', 'hidden').css('display', 'block')
        $('.qiniu').click(function(){
            var $input = $('input', this)
            if ($input.prop('disabled')) {
                return
            }
            var $img = $('.qiniu-preview', this)
            uploadToQiniu({
                uploadUrl: 'https://up-z2.qbox.me',//'http://up-z2.qiniu.com/',
                token: qn.upload_token,
                domain: qn.domain,
                callback: function(url) {
                    $input.val(url)
                    $img.attr('src', url).removeClass('qiniu-empty')
                }
            })
        })
    })
})
