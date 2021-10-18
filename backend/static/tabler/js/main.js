
function detail(obj){

    var target = $(obj).data('target')
    var id = $(obj).data('id')
    if (id){
        window.choiceType = true
    }else{
        window.choiceType = false
    }
    window.obj = obj
    $.ajax({
        type: 'GET',
        url: target,
        data: {'id': id},
        async: true,
        dataType: 'html',
        success: function(html){
            $('.modal-dialog').empty();
            $('.modal-dialog').append(html);
            $('.modal').modal('show')
        }
    })

}

function gotoList(data){

    var a = (document.referrer || '?').split('?')
    console.log(a)
    var params = a[1]
    var parm_list = new URLSearchParams(params)
    parm_list.set('msg', data.msg)
    var kw = parm_list.entries()
    var url = '?'
    for (let i of kw) {
        console.log(i)

        url += '&' + i[0] + '=' + i[1]

    }

    location.href = a[0] + url

}

function ajaxSubmitForm(obj){

    $.ajax({  
        type: obj.attr('method'),  // 提交的方法
        url: obj.attr('action'),   // 提交的地址  
        data: obj.serialize(),     // 序列化表单参数 
        async: true,
        error: function(request) {  // 失败的话
            alert("服务器出错");  
        },  
        success: function(data) {  // 成功
           if (data.errcode == 0){
               // 去掉返回上一页
               if (data.data.order_page === 1){
                   window.location.href = "/backend/order/list"
               }
               else if (data.data.re === 0){
                   window.location.reload();
               }else{
                   gotoList(data.data);
               }
           }else{
                var html = repAlert(data.msg, 'danger') 
                $('.dimmer').removeClass('active')
                $('.show-alert').html(html)
                $("html, body").animate({ scrollTop: "0px" });
           }
            
        }  
     });
}

function ajaxModal(obj, func){

    $.ajax({  
        type: obj.attr('method'),  // 提交的方法
        url: obj.attr('action'),   // 提交的地址  
        data: obj.serialize(),     // 序列化表单参数 
        async: true,
        error: function(request) {  // 失败的话
            alert("服务器出错");  
        },  
        success: function(data) {  // 成功
           if (data.errcode == 0){
                func(data)
           }else{
                var html = repAlert(data.msg, 'danger') 
                $('.dimmer').removeClass('active')
                $('.error-msg').html(html)
                $("html, body").animate({ scrollTop: "0px" });
           }
            
        }  
     });
}

function closeModal() {
    $('.modal-dialog').empty();
    $('.modal').modal('hide')
}

function repAlert(msg, type){

    var str = '<div class="alert alert-'+ type +' alert-dismissable" role="alert">'+
        '<span class="alert-content">'+ msg +
        '</span><button data-dismiss="alert" class="close"></button></div>'

    return str
}

function ajaxSubmitStore(obj){

    $.ajax({  
        type: obj.attr('method'),  // 提交的方法
        url: obj.attr('action'),   // 提交的地址  
        data: obj.serialize(),     // 序列化表单参数 
        async: true,
        error: function(request) {  // 失败的话
            alert("服务器出错");  
        },  
        success: function(data) {  // 成功
            $('.modal').modal('hide')
            if (data.errcode == 0){

                if (window.choiceType == true){ // 修改门店

                    var td = window.obj.parent().parent().children()
                    $(td).eq(1).html(data.data.name)
                    $(td).eq(2).html(data.data.address)
                    $(td).eq(3).html(data.data.phone)

                }else{ // 添加门店

                    if (data.data.is_backend){
                        var str = "<tr class='store'>" +
                                "<td>" + data.data.count + "</td>" +
                                "<td>" + data.data.name + "</td>" +
                                "<td>" + data.data.address + "</td>" +
                                "<td>" + data.data.phone + "</td>" +
                                "<td>" +
                                    "<a href='javascript: void(0)' data-target='/backend/store/detail' data-id='" + data.data.id + "' class='detail'> 详情 </a>" +
                                    "<a href='javascript: void(0)' data-target='/backend/store/del' data-id='" + data.data.id + "' class='del'> 删除 </a>" +
                                "</td>"+
                            "</tr>"
                    }else{
                        var str = "<tr class='store'>" +
                                "<td>" + data.data.count + "</td>" +
                                "<td>" + data.data.name + "</td>" +
                                "<td>" + data.data.address + "</td>" +
                                "<td>" + data.data.phone + "</td>" +
                                "<td>" +
                                    "<a href='javascript: void(0)' data-target='/business/store/detail' data-id='" + data.data.id + "' class='detail'> 详情 </a>" +
                                    "<a href='javascript: void(0)' data-target='/business/store/del' data-id='" + data.data.id + "' class='del'> 删除 </a>" +
                                "</td>" +
                            "</tr>"
                    }
                    
                    window.obj.parent().parent().before(str)

                }
                
            }else{
                alert("操作失败");
            }
        }  
     });
}

$(function(){

    $('.modal-dialog').on('submit', '.ajax-store', function(){

        ajaxSubmitStore($(this))
        return false
    })
    $('.ajax-form').submit(function(){
        
        $('.dimmer').addClass('active')
        ajaxSubmitForm($(this))
        return false
    })

    $('tbody').on('click', '.detail', function(){
        detail($(this))
    })

    $('#bus_info').click(function(){
        $.ajax({
            type: 'GET',
            url: '/business/business/info',
            dataType: 'html',
            success: function(html){
                $('.modal-dialog').empty();
                $('.modal-dialog').append(html);
                $('.modal').modal('show')
            }
        })
    })

    $('.activity-qrcode').click(function(){
        
        var src = this.dataset.src
        $('.modal-dialog').empty();
        $('.modal-dialog').append('<img class="big-qrcode" src="'+ src +'">');
        $('.modal').modal('show')

    })

    $('.qrcode').click(function(){
        
        var src = $(this).attr('src')
        $('.modal-dialog').empty();
        $('.modal-dialog').append('<img class="big-qrcode" src="'+ src +'">');
        $('.modal').modal('show')

    })

    $('.show-img').click(function(){
        
        var src = $(this).attr('src')
        $('.modal-dialog').empty();
        $('.modal-dialog').append('<img class="modal-img" src="'+ src +'">');
        $('.modal-show-img').modal('show')

    })


    $('tbody').on('click', '.del', function(){
        var choice = confirm('确定删除?')
        var $this = this
       if (choice){
            var target = $(this).data('target')
            var id = $(this).data('id')
            $.ajax({
                type: 'GET',
                url: target,
                data: {'id': id},
                success: function(data){
                    if (data.errcode == 0){
                        $($this).parent().parent().remove()
                    }else{
                        alert(data.data.msg);
                    }
                }
            })
            
       }
    })

    $('.recharge').click(function(){

        var id = this.dataset.id
        var balance = prompt('请输入充值金额(元)')
        var re = /^[+-]?([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?$/
        if (re.test(balance)){
            $.post('/backend/business/recharge', {id: id, balance: balance}, function(data){

                if (data.errcode == 0){
                    alert('充值成功.')
                    $('.balance-' + id).text(data.data.balance)
                }else{
                    alert('充值失败，' + data.msg)
                }
            
            })
        }
        else if (balance){
            alert('请输入纯数字')
        }
        
    })

    $('.selecte').change(function(){
        
        if (this.value == 'true'){
            $('.reason').removeClass('display-none')
        }else {
            $('.reason').addClass('display-none')
        }
    })
    
});
