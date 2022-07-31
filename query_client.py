from socket import socket

POST=8888
STR="127.0.0.1"
ADDR=(STR,POST)
class Operation:
    def __init__(self):
        self.name=""
    def user_log(self,sock,request,tishi):
        while True:
            user_name = input("请输入用户名:")
            self.name=user_name
            user_password = input("请输入密码:")
            log="%s %s %s"%(request,user_name,user_password)
            #发送请求
            sock.send(log.encode())
            #接收请求
            date = sock.recv(1024).decode()
            if date == "OK":
                print(tishi)
                return
            else:
                print('你输入的用户名或密码有误')
    def qust(self,sock:socket):
        while True:
            wrd=input("请输入单词:")
            if wrd == "##":
                return
            msg='QUERY %s %s'%(self.name,wrd)
            sock.send(msg.encode())
            date=sock.recv(1024).decode()
            if date != 'FAIL':
                print(date)
            else:
                print("单词不存在")
    def chalishi(self,sock:socket):
        sock.send(b"HIST")
        while True:
            date=sock.recv(1024)
            if date.decode()=='##':
                break
            print(date.decode())
class uid:
    def __init__(self):
        self.operation=Operation()
    def one_uid(self):
        one="""
        ============ 单词查询系统 ============
                1.登录  2.注册  3.退出
        """
        print(one)
    def tow_udi(self):
        tow="""
        ============ 单词查询系统 ============
                1.查询  2.历史记录  3.注销
        """
        print(tow)
    def main(self):
        sock = socket()
        sock.connect(ADDR)
        while True:
            while True:
                self.one_uid()
                one_inp=input("功能选择：")
                if one_inp == "1":
                    self.operation.user_log(sock,"LOG","登录成功")
                    break
                elif one_inp=="2":
                    self.operation.user_log(sock,'REGI',"成功注册")
                elif one_inp=="3":
                    return
                else:
                    print('请输入正确选项')
            while True:
                self.tow_udi()
                user_que = input("输入需要的功能:")
                if user_que == "1":
                    self.operation.qust(sock)
                elif user_que == "2":
                    self.operation.chalishi(sock)
                elif user_que == "3":
                    break
        sock.close()
if __name__ == '__main__':
    uids=uid()
    uids.main()