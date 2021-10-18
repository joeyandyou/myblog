require(['jquery'], function($){
    $.fn.extend({valueCent: function(){
        var $cent = this
        this.attr('step', '0.01').each(function(){
            var $this = $(this)
            if ($this.val()) {
                $this.val(parseInt($this.val()) / 100)
            }
        }).parents('form').submit(function(){
            $cent.each(function(){
                var $this = $(this)
                $this.val(parseInt(parseFloat($this.val()) * 100))
            })
        })
    }})
    $(function(){
        $(window.cent_selector || '#id_price,.value_cent').valueCent()
    })
});

function centSelect(selector) {
    window.cent_selector = selector;
}