$(function(){
    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        // ['blockquote', 'code-block'],

        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        // [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        // [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent

        // [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'align': [] }, 'clean', 'image'],
    ]

    Quill.register(Quill.import('attributors/style/direction'), true);
    Quill.register(Quill.import('attributors/style/align'), true);
    Quill.register(Quill.import('attributors/style/size'), true);

    // 预填充值
    $('.richeditor').each(function(){
        var $this = $(this)
        var quill = new Quill(this, {
            theme: 'snow',
            modules: {
                toolbar: {
                    container: toolbarOptions,
                    handlers: {
                        // handlers object will be merged with default handlers object
                        image: function(value) {
                            uploadToQiniu({
                                uploadUrl: 'https://up-z2.qbox.me',//'http://up-z2.qiniu.com/',
                                token: qn.upload_token,
                                domain: qn.domain,
                                callback: function(url) {
                                    var span = quill.getSelection()
                                    quill.deleteText(span.index, span.length)
                                    quill.insertEmbed(span.index, 'image', url)
                                }
                            })
                        }
                    }
                },
            },
        })
        var value = $('#id_' + $this.data('input')).val()
        let richtext_object = this.__quill.root
	if (value) {
            this.__quill.root.innerHTML = value
        }

        $this.parents('form').submit(function(){
            // $('#id_' + $this.data('input')).val(this.__quill.root.innerHTML)
	    $('#id_' + $this.data('input')).val(richtext_object.innerHTML)
        })
    })
})
