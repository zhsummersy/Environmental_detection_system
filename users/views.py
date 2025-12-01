from django.shortcuts import render, redirect,HttpResponse
from users.models import *
from rest_framework.parsers import JSONParser
from django.http import JsonResponse  
from django.core import serializers 
import sqlite3  

def index(request):
    data = SensorData.objects.all().order_by('-id')
    chartData = SensorData.objects.all().order_by('-id')[:13]
    return render(request, 'index.html',{'data':data,'chartData':chartData})

def chart(request):
    data = SensorData.objects.all().order_by('-id')[:13]
    return render(request, 'charts.html',{'data':data})

def table(request):
    alertData = Alert.objects.all().order_by('-Alertid')
    return render(request, 'tables.html',{'alertData':alertData})

def fan(request):
    return render(request, 'fan.html')

def FanZT(request):
    fan_obj = Fan.objects.get(id=1)  
    zt_value = fan_obj.zt  
    print(zt_value)
    return HttpResponse(zt_value)

def FanStart(request):
    conn = sqlite3.connect('db.sqlite3')  
    cur = conn.cursor()   
    motor_sql = "update users_fan set zt = 'open'"
    cur.execute(motor_sql)
    conn.commit() 
    motor = cur.fetchall()
    conn.close() 
    print('风机开启')
    return HttpResponse('open')

def FanStop(request):
    conn = sqlite3.connect('db.sqlite3')  
    cur = conn.cursor()   
    motor_sql = "update users_fan set zt = 'close'"
    cur.execute(motor_sql)
    conn.commit() 
    motor = cur.fetchall()
    conn.close() 
    print('风机关闭')
    return HttpResponse('stop')

def warn(request):
    return render(request, 'warn.html')

def login(request):
    if  request.COOKIES.get('username'):
        print('用户已登陆')
        return redirect("/")
    if request.method == 'GET':
        print('login')
        return render(request, 'login.html')
    # 用户登录信息判断,如果登录账号密码正确:
    else:
        # 获取用户登录信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        # 查询用户信息，数据库字段对应
        user = webuser.objects.filter(
            username=username, password=password).first()
        # user = webuser.objects.raw("select id,username,password from users_webuser where username = %s",[username])
        if user is None:
            # return render(request,'login.html',{'script':'alert','wrong':'用户名或密码错误'})
            return render(request, 'login.html', {'code': 1, 'message': '用户名或密码错误'})
        if user:
            userid = user.userid
            print(userid)
            rep = redirect('/')
            rep.set_cookie('username', username, expires=60*60*24*7)
            rep.set_cookie('userid', userid, expires=60*60*24*7)
            return rep
    rep = render(request, 'index.html', context={'username': username})
    return rep

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # post方法获取值
        username = request.POST.get('username')
        user = webuser(username=request.POST.get('username'),
                       password=request.POST.get('password'),
                       email=request.POST.get('email'),
                       age=request.POST.get('age'),
                       hobby = '',
                       kind = '休闲',
                    #    hobby=request.POST.get('hobby'),
                    #    kind=request.POST.get('kind'),
                       )
        user.save()
        rep = redirect('/login')
        # rep.set_cookie('username', username, expires=60*60*24*7)
        return rep


def userpage(request):
    # 需要登录
    if not request.COOKIES.get('username'):
        return redirect("/login")
    # 显示信息
    if request.method == 'GET':
        # 通过cookies获取用户id
        userid = request.COOKIES.get('userid')
        print(userid)
        user_info = webuser.objects.filter(userid=userid)
        return render(request, 'userpages.html',
                      {'user_info': user_info})
    else:
        # 提交表单更新信息
        # user = request.COOKIES.get('username')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        age = request.POST.get('age')
        kind = ''
        print(username)
        print(email)
        print(password)
        print(age)
        print(kind)
        webuser.objects.filter(username=username).update(
            username=username, email=email, password=password, age=age, kind=kind)
        return redirect("/")


def outlogin(request):
    rep = redirect('/')
    # 去除名为username的cookies
    rep.delete_cookie("username")
    return rep


def getMax(request):
     # 获取Threshold模型的数据  
    threshold_data = Threshold.objects.values('threshold', 'indicator')   
  
    # 将数据转换为JSON格式  
    json_data = list(threshold_data)  
    print(json_data)
    # 返回JSON响应  
    return JsonResponse(json_data, safe=False)

def upload(request):
    if request.method == 'GET':
        return HttpResponse('404')
    else:
        data = JSONParser().parse(request)
        print(data)
        c = SensorData(
                   co_concentration = data['co'],
                   h2s_concentration = data['h2s'],
                   methane_concentration = data['ch4'],
                   ammonia_concentration = data['nh3'],
                   water_level = data['height'],
                   )

        c.save()
        return HttpResponse('Server has received upload')

def alert(request):
    if request.method == 'GET':
        return HttpResponse('404')
    else:
        data = JSONParser().parse(request)
        print(data)
        print(data)
        c = Alert(
                   content = data['content'],
                   value = data['value'],
                   )
        c.save()
        return HttpResponse('alert received')


