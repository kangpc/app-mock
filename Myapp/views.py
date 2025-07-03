import json
import os
import re
import threading
import time
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from Myapp.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import shutil
import subprocess
# Create your views here.
# 进入项目列表
@login_required()
def project_list(request):
    project_qs = DB_project.objects.all()
    buttons =  [{"name":"新增项目","href":"/add_project/","icon":"folder"},
               {"name":"项目数据","href":"javascript:project_data()","icon":"database"}]
    page_name = "项目列表页"
    return render(request,'project_list.html',{"projects":project_qs,"buttons":buttons,"page_name":page_name})

# 删除项目
def del_project(request,pid):
    DB_project.objects.filter(id=pid).delete()
    DB_mock.objects.filter(project_id=pid).delete()
    try:
        os.remove('Myapp/mitm_edits/%s_mitm_edit.py'%pid)
    except:
        ...
    return HttpResponseRedirect('/project_list/')

# 增加项目
def add_project(request):
    project = DB_project.objects.create(name='新项目',creater=request.user.username)
    shutil.copy('Myapp/mitm_edits/mitm_edit.py','Myapp/mitm_edits/%s_mitm_edit.py'%project.id)
    return HttpResponseRedirect('/project_list/')

# 保存项目
def save_project(request):
    new_name = request.GET['new_name']
    black_hosts = request.GET['black_hosts']
    white_hosts = request.GET['white_hosts']
    project_id = request.GET['project_id']
    DB_project.objects.filter(id=project_id).update(name=new_name,black_hosts=black_hosts,white_hosts=white_hosts)
    return HttpResponse('')

# 获取项目数据
def project_data(request):
    res = ''
    projects = DB_project.objects.all()
    for project in projects:
        res += '【'+ str(project.id) + '】'
        res += project.name +' '
        res += project.creater

        # 单元数量
        res +='【'+ str(len(DB_mock.objects.filter(project_id=project.id)))+ '】'

        res += '【'+ str(project.run_counts) + '】'
        res += '【' + str(project.mock_counts) + '】'
        res += '<br>'
    return HttpResponse(res)

# 进入登录页面
def login(request):
    return render(request,'login.html')  #返回登录页面

# 登录
def sign_in(request):
    # 获取来自页面用户输入的用户名和密码
    a = request.POST['in_username']
    b = request.POST['in_password']
    # 去数据库用户表中查询真假
    user = auth.authenticate(username=a,password=b)
    # 如果为假，不登录，重新返回登录页面
    if user is None:
        # return HttpResponse('密码错误')
        return HttpResponse('0')
     # 如果为真，登录，跳转到项目列表页
    else:
        auth.login(request,user)
        request.session['user'] = a
        return HttpResponse('1')

# 退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

# 注册
def sign_up(request):
    # 获取用户名 密码 邮箱
    a = request.GET['up_username']
    b = request.GET['up_password']
    c = request.GET['up_email']
    # 注册
    try:# 注册成功
        user = User.objects.create_user(username=a,email=c,password=b)
        user.save()
        auth.login(request,user)
        request.session['user'] = a
        return HttpResponseRedirect('/project_list/')
    except:
        # 注册失败
        return HttpResponseRedirect('/login/')

# 重设密码
def reset_password(request):
    # 获取用户名，验证码，新密码
    username = request.GET['fg_username']
    code = request.GET['fg_code']
    password = request.GET['fg_password']
    # 判断验证码
    if code == User.objects.filter(username=username)[0].last_name:
        User.objects.filter(username=username).update(password=make_password(password))
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse('code is wrong!')

# 发送验证码邮件
def send_email_pwd(request):
    # 获取用户名
    username = request.GET['username']
    # 根据用户名去用户表找出他的邮箱
    email = User.objects.filter(username=username)[0].email
    # 生成随机验证码
    code = str(random.randint(1000,9999))
    # 保存验证码
    User.objects.filter(username=username).update(last_name=code)
    # 发送邮件
    msg = '这是您找回密码的验证码：'+code
    send_mail('mock平台找回密码',msg,settings.EMAIL_FROM,[email])
    # 返回yes
    return HttpResponse('yes')

# 进入Mock列表页
def mock_list(request,project_id):
    # 从数据库拿出符合的mock列表
    a = DB_mock.objects.filter(project_id = project_id)
    # 根据项目id去数据库找出来这个项目
    project = DB_project.objects.filter(id=project_id)[0]
    # 拿到当前平台ip
    try:
        import socket
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    res = {}
    res['mocks'] = a
    res['buttons'] = [{"name": "新增单元", "href": "/add_mock/%s/"%project.id, "icon": "folder"},
               {"name": "抓包导入", "href": "javascript:show_catch()", "icon": "hand-o-right"},
               {"name": "项目设置", "href": "javascript:project_set()", "icon": "edit"},
               {"name": "启动服务", "href": "/server_on/%s/"%project_id, "icon": "hourglass-start"},
               {"name": "关闭服务", "href": "/server_off/%s/"%project_id, "icon": "hourglass-end"},
               ]
    res['page_name'] = "项目详情页:【%s】"%project.name+' 【host】:'+ip+' 【port】: '+str(9000+int(project_id))
    res['project_state'] = '服务状态：'+ str(project.state)
    res['project_id'] = project_id
    res['project'] = project
    return render(request,'mock_list.html',res)

# 新增mock单元
def add_mock(request,project_id):
    DB_mock.objects.create(name='新单元',project_id=project_id)
    return HttpResponseRedirect('/mock_list/%s/'%project_id)

# 删除mock单元
def del_mock(request,mock_id):
    mocks = DB_mock.objects.filter(id=mock_id)
    project_id = mocks[0].project_id
    mocks.delete()
    return HttpResponseRedirect('/mock_list/%s/'%project_id)

# 保存mock单元
def save_mock(request):
    mock_id = request.GET['mock_id']
    mock_name = request.GET['mock_name']
    catch_url = request.GET['catch_url']
    mock_response_body = request.GET['mock_response_body']
    model = request.GET['model']
    response_headers = request.GET['response_headers']
    state_code = request.GET['state_code']
    mock_response_body_lj = request.GET['mock_response_body_lj']
    mock_time = request.GET['mock_time']
    DB_mock.objects.filter(id=mock_id).update(name=mock_name,
                                              catch_url=catch_url,
                                              mock_response_body=mock_response_body,
                                              model=model,
                                              response_headers = response_headers,
                                              state_code = state_code,
                                              mock_response_body_lj = mock_response_body_lj,
                                              mock_time = mock_time,
                                              )
    return HttpResponse('')

# 获取数据
def get_mock(request):
    mock_id = request.GET['mock_id']
    mock = DB_mock.objects.filter(id=mock_id).values()[0]
    res = {"mock":mock}
    return HttpResponse(json.dumps(res),content_type='application/json')

# 启用单元
def mock_on(request,mock_id):
    mock = DB_mock.objects.filter(id=mock_id)
    mock.update(state=True)
    project_id = mock[0].project_id
    return HttpResponseRedirect('/mock_list/%s/'%project_id)

# 弃用单元
def mock_off(request,mock_id):
    mock = DB_mock.objects.filter(id=mock_id)
    mock.update(state=False)
    project_id = mock[0].project_id
    return HttpResponseRedirect('/mock_list/%s/' % project_id)

# 启动服务
def server_on(request,project_id):
    import threading
    def abc():
        port = str(9000+int(project_id))
        script = 'Myapp/mitm_edits/'+project_id+'_mitm_edit.py'
        cmd = 'nohup mitmdump -p %s -s %s '%(port,script)
        subprocess.call(cmd,shell=True)
    t = threading.Thread(target=abc)
    t.start()
    DB_project.objects.filter(id=project_id).update(state=True)
    return HttpResponseRedirect('/mock_list/%s/'%project_id)

# 关闭服务
def server_off(request,project_id):
    port = str(9000+int(project_id))
    cmd = 'ps -ef|grep mitm |grep %s'%port
    res = subprocess.check_output(cmd,shell=True)
    for i in str(res).split('\\n'):
        if project_id+'_mitm_edit.py' in i:
            pid = max([int(i) for i in re.findall(r'\d+',i.split('/')[0])])
            cmd2 = 'kill -9 %s'%str(pid)
            subprocess.check_output(cmd2,shell=True)
            print('进程已杀死！')
            break
    else:
        print('进程未找到！')
    DB_project.objects.filter(id=project_id).update(state=False)
    return HttpResponseRedirect('/mock_list/%s/'%project_id)


# 获取抓包日志 每秒运行一次
def get_catch_log(request):
    project_id = request.GET['project_id']
    project = DB_project.objects.filter(id=project_id)
    project.update(catch = True) #打开开关
    catch_log = eval(project[0].catch_log) # 字符串列表类型
    ret = {"res":catch_log}
    # 删除原有记录
    project.update(catch_log='[]',catch_time=str(time.time())[:10])
    return HttpResponse(json.dumps(ret),content_type='application/json')

# 导入请求
def import_catch(request):
    project_id = request.POST['project_id']
    chose_catch = json.loads(request.POST['chose_catch'])
    DB_mock.objects.create(project_id=project_id,
                           name=chose_catch['url'][:500],
                           catch_url='/'.join(chose_catch['url'].split('?')[0].split('/')[3:]),
                           response_headers = chose_catch['response_headers'],
                           mock_response_body_lj = chose_catch['response_content']
                           )
    return HttpResponse('')

