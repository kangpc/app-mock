from django.contrib import admin
from django.urls import path,re_path
from Myapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('project_list/',project_list),  #对应后端函数：后端函数写在哪，怎么引用到这，函数内要做什么，函数要怎么写。
    re_path('del_project/(?P<pid>.+)/',del_project),#删除项目
    path('',project_list),# 进入首页项目列表
    path('add_project/',add_project),# 增加项目
    path('save_project/',save_project),# 保存项目
    path('project_data/',project_data),# 获取所有项目数据

    ########
    path('login/',login),# 进入登录页面
    path('accounts/login/',login),# 当忘记带登录态的时候访问的登录页
    ########
    path('sign_in/',sign_in),# 登录动作
    path('sign_up/',sign_up), #注册动作
    path('logout/',logout),# 退出
    path('reset_password/',reset_password),# 重设密码
    path('send_email_pwd/',send_email_pwd),# 发送验证码邮件
    #########
    re_path('mock_list/(?P<project_id>.+)/',mock_list),#进入项目详情页(mock列表页)
    re_path('add_mock/(?P<project_id>.+)/',add_mock),# 新增单元
    re_path('del_mock/(?P<mock_id>.+)/', del_mock),  # 删除单元
    path('save_mock/',save_mock),# 保存单元
    path('get_mock/',get_mock),# 获取mock单元的最新数据
    re_path('mock_on/(?P<mock_id>.+)/',mock_on),# 启用mock单元
    re_path('mock_off/(?P<mock_id>.+)/',mock_off),# 弃用mock单元
    ######
    re_path('server_on/(?P<project_id>.+)/',server_on),# 启动服务
    re_path('server_off/(?P<project_id>.+)/', server_off),  # 关闭服务
    path('get_catch_log/',get_catch_log) , # 获取抓包日志
    path('import_catch/',import_catch),# 导入请求
]
