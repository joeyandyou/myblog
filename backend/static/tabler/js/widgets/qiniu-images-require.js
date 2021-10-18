require.config({
    paths: {
        'qiniu': '/static/tabler/js/widgets/qiniu',
    }
})
require(['jquery', 'qiniu'], function($){
    $(function(){
        $('.qiniu-multi').each(function(){

            var $root = $(this)
            var $input = $($root.data('input'))
            var $group = $root.find('.qiniu-preview-group')
            var $template = $root.find('.qiniu-preview-wrap.template')

            $root.find('input').attr('type', 'hidden').css('display', 'block')
            function calc_urls(){
                $input.val($group.find('.qiniu-preview').map(function(){return this.src}).toArray().join(','))
            }
            
            function preview_click(){
                var $img = $(this)
                uploadToQiniu({
                    uploadUrl: 'https://up-z2.qbox.me',//'http://up-z2.qiniu.com/',
                    token: qn.upload_token,
                    domain: qn.domain,
                    callback: function(url) {
                        $img.attr('src', url)
                        calc_urls()
                    }
                })
            }
            $root.find('.qiniu-preview').click(preview_click)
            $root.find('.qiniu-remove').click(function(){
                $(this).parents('.qiniu-preview-wrap').remove()
                calc_urls()
            })
            $root.find('.qiniu-add').click(function(){
                uploadToQiniu({
                    uploadUrl: 'https://up-z2.qbox.me',//'http://up-z2.qiniu.com/',
                    token: qn.upload_token,
                    domain: qn.domain,
                    callback: function(url) {
                        var $node = $template.clone(true).removeClass('template')
                        $group.append($node)
                        $node.find('.qiniu-preview').attr('src', url).click(preview_click)
                        calc_urls()
                    }
                })
            })
        })
    })
})
