require(['jquery'], function($){
    var $flag = $('.flag-input')
    $flag.each(function(){
        var $this = $(this)
        var $input = $this.find('input[type=hidden]')
        var $items = $this.find('.flag-item')
        var value = parseInt($input.val())
        $items.each(function(){
            this.checked = value & parseInt(this.value)
        })
    }).parents('form').submit(function(){
        $flag.each(function(){
            var $this = $(this)
            var $input = $this.find('input[type=hidden]')
            var $items = $this.find('.flag-item')
            var value = 0
            $items.each(function(){
                if (this.checked) {
                    value |= parseInt(this.value)
                }
            })
            $input.val(value)
        })
    })
})