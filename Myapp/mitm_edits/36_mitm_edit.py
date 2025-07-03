import json
import time
import threading
from mitmproxy import http
import django
import os,sys
sys.path.append("/Users/yiyan/AppMock")
os.environ.setdefault("DJANGO_SETTINGS_MODULE","AppMock.settings")
django.setup()
from Myapp.models import *

def filter(flow):
    project_id = os.path.basename(__file__).split('_')[0]
    project = DB_project.objects.filter(id=project_id)[0]
    if project.white_hosts != '':
        if flow.request.url not in project.white_hosts.split(','):
            return False
    if project.black_hosts != '':
        if flow.request.url in project.black_hosts.split(','):
            return False

def write_catch_log(flow):
    project_id = os.path.basename(__file__).split('_')[0]
    project = DB_project.objects.filter(id=project_id)
    # 读取开关
    catch = project[0].catch
    if catch == True:
        old = eval(project[0].catch_log)
        tmp_header = {}
        for k,v in flow.response.headers.items():
            tmp_header[k]=v
        tmp = {"method":flow.request.method,
               "url":flow.request.url,
               "response_headers":json.dumps(tmp_header),
                "response_content":flow.response.text}
        old.append(tmp)
        project.update(catch_log=str(old))

def request(flow):
    '在请求发送到服务器之前进行干预的脚本'
    # 筛选host
    if filter(flow) == False:
        return
    # 拦截模式
    project_id = os.path.basename(__file__).split('_')[0]

    mocks = DB_mock.objects.filter(project_id=project_id, state=True)
    for m in mocks:
        if m.catch_url in flow.request.url:  # 中了这个mock单元
            print('中了request')
            if m.model == 'lj':
                flow.response = http.HTTPResponse.make(
                    m.state_code,
                    m.mock_response_body_lj,
                    json.loads(m.response_headers)
                )
            break

def response(flow):
    '在请求从服务器返回后进行干预的脚本'
    # 筛选host
    if filter(flow) == False:
        return
    # 放行模式
    project_id = os.path.basename(__file__).split('_')[0]
    mocks = DB_mock.objects.filter(project_id = project_id,state=True)
    for m in mocks:
        if m.catch_url in flow.request.url: #中了这个mock单元
            print('中了response')
            if m.model == 'fx':
                all_updatas = m.mock_response_body.split('\n')
                for u in all_updatas:
                    if '=>' in u:# 是普通替换规则
                        try:
                            json.loads(flow.response.text)
                            flow.response.text = json.dumps(json.loads(flow.response.text),ensure_ascii=False)
                        except:
                            ...
                        flow.response.text = flow.response.text.replace(u.split('=>')[0].rstrip(),u.split('=>')[1].lstrip())
                    elif '=' in u:# 是json路径替换规则
                        try:
                            old = json.loads(flow.response.text)
                        except:
                            continue
                        key = u.split('=')[0].rstrip()
                        value = eval(u.split('=')[1].lstrip())
                        tmp_cmd = ''
                        for i in key.split('.'):
                            try:
                                int(i)
                                tmp_cmd += '[%s]' % i
                            except:
                                tmp_cmd += '[%s]' % repr(i)
                        end_cmd = "old" + tmp_cmd + "=value"
                        try:
                            exec(end_cmd)
                        except:continue
                        flow.response.text = json.dumps(old)
                    else: # 不符合规则的
                        ...
                # 更新返回头
                for k,v in json.loads(m.response_headers).items():
                    flow.response.headers[str(k)] = str(v)

            ### 时间控制
            try: # 0 , '', '一'，'qwe'
                mock_time = float(m.mock_time)
            except:
                mock_time = 0
            passtime = float(time.time()) - float(flow.request.timestamp_start)
            if mock_time > passtime:
                cha = mock_time-passtime
                time.sleep(cha)
            break

    # 写入log
    t = threading.Thread(target=write_catch_log,args=[flow,])
    t.setDaemon(True)
    t.start()

