from django.http import HttpResponse, JsonResponse

from app.models import url

import redis
import json
 
def indexHandler(request):
    return HttpResponse("hello")

def changeBase(n, b):
    """
    进制转换 （十进制转任意）
    """
    baseList = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    x,y = divmod(n,b)
    if x>0:
        return changeBase(x,b) + baseList[y]
    else:             
        return baseList[y]

def longToShortHandler(request):
    """
    长地址转短地址
    """
    if request.method == 'GET':
        ret = {'message': 'Please use post'}
        return JsonResponse(ret)
    if request.method == 'POST':
        # 获取长地址
        longUrl = request.POST.get('longUrl', '')

        # 从redis中拉自增id
        pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=4)
        r = redis.StrictRedis(connection_pool=pool)
        urlNum = r.get('id')
        r.incr('id')

        # 生成短地址
        shortUrl = str(changeBase(int(urlNum), 62))

        # 写入mysql
        u = url(shortUrl=shortUrl, longUrl=longUrl)
        u.save()

        ret = {'shortUrl': shortUrl}
        return JsonResponse(ret)
    
def shortToLongHandler(request):
    """
    短地址转长地址
    """
    if request.method == 'GET':
        ret = {'message': 'Please use post'}
        return JsonResponse(ret)
    if request.method == 'POST':
        # 获取短地址
        shortUrl = request.POST.get('shortUrl', '')

        # mysql中获取对应长地址
        res = url.objects.filter(shortUrl=shortUrl)
        if len(res) == 0:
            # 未找到数据
            ret = {'longUrl': None}
            return JsonResponse(ret)

        # 获取长地址
        longUrl = res[0].longUrl

        ret = {'longUrl': longUrl}
        return JsonResponse(ret)