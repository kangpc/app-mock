# AppMock - HTTP API Mock 服务平台

## 项目概述

AppMock 是一个基于 Django 和 mitmproxy 的 HTTP API Mock 服务平台，专为 API 接口测试和开发调试而设计。通过中间人代理技术，提供灵活的 API 请求拦截、模拟和响应修改功能。

## 主要功能

### 🔐 用户管理系统
- 用户注册/登录
- 密码重置（支持邮件验证码）
- 会话管理

### 📁 项目管理
- 多项目支持，每个项目独立运行
- 项目配置（黑白名单域名过滤）
- 项目数据统计（运行次数、Mock 次数等）

### ⚙️ Mock 单元管理
- **拦截模式（lj）**: 完全拦截请求，返回预设的静态响应
- **放行模式（fx）**: 允许请求通过，但可修改响应内容
- 支持配置：
  - 响应状态码
  - 响应头
  - 响应体内容
  - 请求延时控制

### 🕷️ 实时抓包功能
- 基于 mitmproxy 的实时网络流量捕获
- 可视化请求/响应查看
- 支持将抓包结果一键导入为 Mock 规则

### 🔧 高级功能
- **域名过滤**: 支持黑白名单机制
- **JSON 路径替换**: 使用路径表达式精确修改 JSON 响应
- **字符串替换**: 简单的文本替换功能
- **时间控制**: 模拟网络延时
- **动态服务管理**: 无需重启，实时启停 Mock 服务

## 技术栈

- **后端框架**: Django 2.2
- **数据库**: SQLite
- **网络代理**: mitmproxy
- **前端**: Bootstrap 3.4.1 + jQuery
- **语言**: Python 3

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   客户端应用      │───▶│   AppMock 代理   │───▶│   真实服务器      │
│                 │    │ (mitmproxy)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Django 管理    │
                       │     后台         │
                       └─────────────────┘
```

## 安装与配置

### 环境要求
- Python 3.6+
- Django 2.2
- mitmproxy

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd AppMock
```

2. **安装依赖**
```bash
pip install django==2.2
pip install mitmproxy
```

3. **数据库配置**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **创建超级用户**
```bash
python manage.py createsuperuser
```

5. **启动开发服务器**
```bash
python manage.py runserver 0.0.0.0:8000
```

### 邮件配置

在 `AppMock/settings.py` 中配置邮件服务器信息：

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'your-email@qq.com'
EMAIL_HOST_PASSWORD = 'your-password'
EMAIL_FROM = 'your-email@qq.com'
```

## 使用指南

### 1. 创建项目

1. 访问 `http://localhost:8000` 并登录
2. 点击"新增项目"创建新的 Mock 项目
3. 配置项目名称和域名过滤规则

### 2. 配置 Mock 规则

#### 拦截模式示例
```
URL 关键字: /api/user
模式: 拦截模式
HTTP 状态码: 200
响应头: {"Content-Type": "application/json"}
响应体: {"status": "success", "data": {"id": 1, "name": "test"}}
```

#### 放行模式示例
```
URL 关键字: /api/user
模式: 放行模式
响应更新策略:
  name=>John Doe          # 字符串替换
  data.user.id=12345      # JSON 路径替换
```

### 3. 启动 Mock 服务

1. 在项目详情页点击"启动服务"
2. 记录显示的代理端口（9000 + 项目ID）
3. 配置客户端使用该代理

### 4. 代理配置

将客户端应用的 HTTP 代理设置为：
- **代理地址**: AppMock 服务器 IP
- **代理端口**: 9000 + 项目ID

### 5. 实时抓包

1. 点击"抓包导入"打开抓包界面
2. 客户端发送请求后，可实时查看请求/响应
3. 选择需要的请求记录，点击"import"导入为 Mock 规则

## 文件结构

```
AppMock/
├── AppMock/                # Django 项目配置
│   ├── settings.py         # 项目配置
│   ├── urls.py            # 主路由配置
│   └── wsgi.py            # WSGI 配置
├── Myapp/                 # 主应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图逻辑
│   ├── templates/         # 页面模板
│   ├── static/            # 静态资源
│   └── mitm_edits/        # mitmproxy 脚本
├── manage.py              # Django 管理脚本
└── db.sqlite3             # SQLite 数据库
```

## 核心数据模型

### DB_project（项目表）
- `name`: 项目名称
- `state`: 服务运行状态
- `black_hosts`: 黑名单域名
- `white_hosts`: 白名单域名
- `catch_log`: 抓包日志数据

### DB_mock（Mock 规则表）
- `catch_url`: 匹配的 URL 关键字
- `model`: 模式（lj-拦截/fx-放行）
- `response_headers`: 响应头配置
- `state_code`: HTTP 状态码
- `mock_response_body`: 放行模式更新规则
- `mock_response_body_lj`: 拦截模式响应体
- `mock_time`: 延时控制

## 高级配置

### 响应修改规则

#### 字符串替换
```
旧字符串=>新字符串
```

#### JSON 路径替换
```
a.b.c=新值
data.user.0.name="John"
response.items.2=[1,2,3]
```

### 时间控制
设置 `mock_time` 参数（秒）来模拟网络延时，如果设置的时间大于实际请求时间，会额外等待差值时间。

## 注意事项

⚠️ **安全警告**
- 本项目仅供开发测试使用
- 生产环境请修改默认密钥
- 建议在受控网络环境中使用

⚠️ **使用限制**
- 每个项目占用一个独立端口
- CSRF 中间件已禁用以支持 API 测试
- 服务启停需要系统权限执行进程管理命令

## 故障排除

### 常见问题

1. **Mock 服务启动失败**
   - 检查端口是否被占用
   - 确认 mitmproxy 已正确安装
   - 检查文件权限

2. **抓包功能不工作**
   - 确认客户端代理配置正确
   - 检查防火墙设置
   - 验证域名过滤规则

3. **响应修改不生效**
   - 检查 URL 关键字匹配规则
   - 验证 JSON 路径语法
   - 确认 Mock 单元已启用

## 开发贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 许可证

[请添加相应的许可证信息] 