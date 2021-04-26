from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# 原生上传文件的方式
from stu.models import Student


def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        # 获取请求参数
        uname = request.POST.get('uname', '')
        photo = request.FILES.get('photo', '')
        import os
        if not os.path.exists('media'):
            os.makedirs('media')
        with open(os.path.join(os.getcwd(), 'media', photo.name), 'wb') as fw:
            # photo.read()一次性读取文件到内存
            # fw.write(photo.read())
            # photo.chuncks()分块读取
            for ck in photo.chunks():
                fw.write(ck)
        return HttpResponse('Success')
    else:
        return HttpResponse('访问量多大，一会再试吧')
    return None


# Django方法
def upload_view(request):
    # 接收请求参数
    uname = request.POST.get('uname', '')
    photo = request.FILES.get('photo', '')
    # 入库操作
    Student.objects.create(sname=uname, photo=photo)
    return HttpResponse('success')


# 显示图片
def showall_view(request):
    # 读取所有学生信息
    stus = Student.objects.all()
    return render(request, 'show.html', {'stus': stus})


def download_view(request):
    # 获取请求参数（图片存储位置）
    photo = request.GET.get('photo', '')
    # 获取文件名
    filename = photo[photo.rindex('/') + 1:]
    # 开启一个流
    import os
    # 获取文件绝对路径
    path = os.path.join(os.getcwd(), 'media', photo.replace('/', '\\'))
    with open(path, 'rb') as fr:
        response = HttpResponse(fr.read())
        response['Content-Type'] = 'image/png'
        # 预览模式
        # response['Content-Disposition'] = 'inline;filename=' + filename
        # 附件模式(谷歌浏览器中，中文名字预览显示，英文名则下载到本地）
        response['Content-Disposition'] = 'attachment;filename=' + filename

    return response
