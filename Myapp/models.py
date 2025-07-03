from django.db import models

# Create your models here.
class DB_project(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True)
    creater = models.CharField(max_length=30,null=True,blank=True)
    run_counts = models.IntegerField(default=0)
    mock_counts = models.IntegerField(default=0)
    state = models.BooleanField(default=False) #服务状态
    catch_log = models.TextField(default='[]')
    catch = models.BooleanField(default=False) # 抓在线日志的开关
    black_hosts = models.CharField(max_length=500,null=True,blank=True,default='') #黑名单
    white_hosts = models.CharField(max_length=500,null=True,blank=True,default='') #白名单,不为空的时候，只放白名单域名
    catch_time = models.CharField(max_length=20,null=True,blank=True,default='') #最后一次在线获取抓包记录的时间戳
    def __str__(self):
        return '项目名字是：'+self.name


    '''
    [{"method":"GET","url":"http://www.baidu.com","response_headers":'{"a":"b"}',"response_content":"我是返回体"},{"method":"GET","url":"http://www.baidu.com","response_headers":'{"a":"b"}',"response_content":"我是返回体"}]
    '''

class DB_mock(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True)
    state = models.BooleanField(default=False)
    project_id = models.CharField(max_length=30,null=True,blank=True)
    catch_url = models.CharField(max_length=500,null=True,blank=True,default='')
    mock_response_body = models.TextField(null=True,blank=True,default='') #放行模式更新策略
    model = models.CharField(max_length=30,null=True,blank=True,default='fx') # 拦截：lj,放行：fx
    response_headers = models.CharField(max_length=500,null=True,blank=True,default='{}')
    state_code = models.IntegerField(default=200)
    mock_response_body_lj = models.TextField(null=True,blank=True,default='') # 拦截模式的写死的返回值
    mock_time = models.FloatField(default=0) # 整个请求周期时间控制 秒
    def __str__(self):
        return self.name

