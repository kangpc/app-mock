import paramiko,time,re
class Linux(object):
    def __init__(self,ip,username,password,timeout=30):
        self.ip=ip
        self.username = username
        self.password = password
        self.timeout = timeout
        self.t = ''
        self.chan = ''
        self.try_times =3
    def connect(self):
        while True:
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username,password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                print(u'连接%s成功' % self.ip)
                print(self.chan.recv(65535).decode('utf-8'))
                return
            except Exception as e:
                if self.try_times != 0:
                    print(u'连接%s失败，进行重试' %self.ip)
                    self.try_times -= 1
                else:
                    print(u'重试后依然失败，结束程序')
                    exit(1)
    def close(self):
        try:self.chan.close()
        except:pass
        try:self.t.close()
        except:pass
    def send(self,cmd):
        time.sleep(1)
        cmd += '\r'
        p = re.compile(r'$')
        result = ''
        self.chan.send(cmd)
        while True:
            time.sleep(0.5)
            ret = self.chan.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            if p.search(ret):
                print(result)
                return result


def ok():
    s = Linux('101.43.153.203','wangzijia','wangzijia')
    s.connect()
    s.send('pwd')
    s.close()


ok()