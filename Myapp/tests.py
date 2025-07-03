
import re

old = {"a":1,"b": {"c":[11,22,33]}}

s = 'b.c.2=55'

key = s.split('=')[0].rstrip().split('.')
value = s.split('=')[1].lstrip()
tmp = ''
for j in key:
    try:
        int(j)
        tmp += '[' + j+']'
    except:
        tmp += '['+repr(j)+']'
print(tmp)
exec('old'+tmp+'=eval(value)')

print(old)

#
# flow.response = http.Response.make(
#                 200,
#                 api.body_0,
#                 json.loads(response__header,encoding='utf-8'),
#             )
#
# def response(flow):
#     project_id = os.path.basename(__file__).split('.')[0]
#     api = find_api(flow,project_id)
#     if api != '':
#         if api.which_model == '1': #确定是放行模式
#             use_time = flow.response.timestamp_end - flow.request.timestamp_start
#             if api != '':
#                 time.sleep(abs(float(api.ntime)-use_time)) # 延迟实际设置
#                 if api.body != '':
#                     try:
#                         flow.response.text = json.dumps(eval(api.body),encoding='utf-8')
#                     except:
#                         flow.response.text = api.body
#         else: # 确定是拦截模式
#             time.sleep(abs(float(api.ntime))) #延迟实际设置
#     try:
#         Mock_catch_apis.objects.create(project_id=project_id,http_status=flow.response.status_code,ctime=time.time()+1,header=str(dict(flow.request.headers)),url=flow.request.url,method=flow.request.method,request_body=flow.request.text,response_body=flow.response.text)
#     except Exception as e:
#         print('接口漏抓:',e)