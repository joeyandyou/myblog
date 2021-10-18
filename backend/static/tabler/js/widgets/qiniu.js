function uploadToQiniu(opt) {
    var params = ['uploadUrl', 'token', 'domain', 'callback']
    params.forEach(function (i) {
        if (!opt[i]) {
            console.warn('uploadToQiniu: 缺少必填参数: ' + i + ' 可能会导致错误！')
        }
    })

    var form = document.getElementById('qiniu-form')
    var fileInput = document.getElementById('qiniu-input')
    var tokenInput = document.getElementById('qiniu-token')

    if (!form) {
        form = document.createElement('form')
        fileInput = document.createElement('input')
        tokenInput = document.createElement('input')

        form.id = 'qiniu-form'
        fileInput.id = 'qiniu-input'
        fileInput.name = 'file'
        fileInput.type = 'file'

        tokenInput.id = 'qiniu-token'
        tokenInput.name = 'token'

        form.appendChild(fileInput)
        form.appendChild(tokenInput)

        fileInput.onchange = function () {
            if (!fileInput.value) {
                return
            }
            var opt = form.opt
            var request = new XMLHttpRequest()
            //监听上传进度
            request.upload.addEventListener('progress', function (event) {
                if (event.lengthComputable) {
                    let progress = Math.ceil(event.loaded * 100 / event.total);
                    document.getElementById('progress').innerText = progress + "%";
                    document.getElementById('video_progress').value = progress;
                }
            });
            request.open('POST', opt.uploadUrl, true)
            request.onload = function () {
                if (request.status !== 200) {
                    return console.log('上传出错')
                }
                // 关闭上传进度
                document.getElementById('video_progress_box').hidden = true;
                var data = JSON.parse(request.responseText)
                var url = opt.domain + data.hash
                opt.callback(url)

                if ((navigator.appVersion.indexOf("MSIE") !== -1)) {
                    var file2 = fileInput.cloneNode(false)
                    file2.onchange = fileInput.onchange
                    fileInput.parentNode.replaceChild(file2, fileInput)
                    fileInput = file2
                } else {
                    fileInput.value = ''
                }
            }
            request.send(new FormData(form))
            // 显示上传进度
            document.getElementById('video_progress_box').hidden = false;
        }
        form.style.display = 'none'
        document.body.appendChild(form)
    }

    tokenInput.value = opt.token
    form.opt = opt
    fileInput.click()
}