require.config({
    shim: {
        'quill': ['jquery', 'quill-core'],
        'richeditor': ['quill', 'qiniu'],
    },
    paths: {
        'quill-core': '/static/tabler/js/widgets/quill.core',
        'quill': '/static/tabler/js/widgets/quill.min',
        'richeditor': '/static/tabler/js/widgets/richeditor',
        'qiniu': '/static/tabler/js/widgets/qiniu',
    }
})
require(['quill', 'richeditor'], function(Quill){
    window.Quill = Quill
})