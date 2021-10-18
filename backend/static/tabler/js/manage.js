require(['jquery', 'selectize'], function($){
    $(function(){
        // 确认操作
        var $action = $('a.action-confirm')
        if ($action.length) {
            var $action_dialog = $('#action-confirm-dialog');
            if ($action_dialog.length) {
                $action.click(function(){
                    var href = this.href;
                    $action_dialog.find('#action-confirm-btn').click(function(){
                        $action_dialog.modal('hide');
                        location.href = href;
                    });
                    $action_dialog.modal('show');
                    return false;
                });
                $action_dialog.on('hidden.bs.modal', function (e) {
                    $action_dialog.find('#action-confirm-btn').unbind('click');
                });
            } else {
                $action.click(function(){
                    return confirm('确认此操作吗');
                });
            }
        }
        // 确认删除
        var $delete = $('a.delete-confirm')
        if ($delete.length) {
            var $dialog = $('#delete-confirm-dialog');
            if ($dialog.length) {
                $delete.click(function(){
                    var href = this.href;
                    $dialog.find('#delete-confirm-btn').click(function(){
                        $dialog.modal('hide');
                        location.href = href;
                    });
                    $dialog.modal('show');
                    return false;
                });
                $dialog.on('hidden.bs.modal', function (e) {
                    $dialog.find('#delete-confirm-btn').unbind('click');
                });
            } else {
                $delete.click(function(){
                    return confirm('确认删除吗');
                });
            }
        }

        $('.form-inline .input-icon-addon').click(function(){
        	$(this).parents('form').submit()
        });
        $('.custom-select').selectize({});
        $('.input-tags').selectize({
            delimiter: ',',
            persist: false,
            create: function (input) {
                return {
                    value: input,
                    text: input
                }
            }
        });
        // 自动提交表单控件
        $('.auto-submit').change(function(){
            $(this).parents('form').eq(0).submit();
        });
        // 保留列表页query参数
        if ($('.keep-query').length > 0) {
            var query = location.search;
            if (query) {
                query = 'query=' + encodeURIComponent(query.substr(1));
                $('.keep-query').each(function(){
                    var $this = $(this);
                    var href = $this.attr('href') || '';
                    href += (href.indexOf('?') != -1 ? '&': '?') + query;
                    $this.attr('href', href);
                })
            }
        }

        $('.linkage').each(function(){
            var $select = $(this)
            var $target = $('#id_' + $select.data('target'))

            $select.change(function() {
                var value = $select.find('option:selected').text()
                $target.val('')

                $target.find('option').each(function(){
                    var $option = $(this)

                    if ($option.text().indexOf(value+':') == 0) {
                        $option.removeAttr('disabled');
                    } else {
                        $option.attr('disabled','disabled')
                    }
                })
            })
        });

        // 自动提交日期表单控件
        $('#statistics_date').change(function(){
            date = $('#statistics_date').val();
            window.location.href = '/backend?date=' + date
        });

        // 自动提交日期表单控件
        $('#statistics_date_bus').change(function(){
            date = $('#statistics_date_bus').val();
            window.location.href = '/business?date=' + date
        });

    })
});
