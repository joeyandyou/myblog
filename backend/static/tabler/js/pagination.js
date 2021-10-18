require(['jquery'], function($){
    var href = location.href;
    if (href.indexOf('?') == -1){
        return false;
    }
    var args = href.substr(href.indexOf('?') + 1).split('&')
    args = args.filter(function(i){ return i.indexOf('page=') == -1 })

    if (args.length) {
        $('.pagination a[href]').each(function(){
            this.href += '&' + args.join('&')
        })
    }
});