import time
from socket import socket
from threading import Thread
import pymysql
# 数据处理类
class Word:
    def __init__(self):
        self.sql=Mysql()
        self.userid=""

    def taget(self,conned:socket):
        while True:
            date = conned.recv(1024)
            if not date:
                break
            msg=date.decode().split(" ",1)
            if msg[0]=="LOG":
                self.look_word(conned,msg[1],self.look_user)
            elif msg[0]=='REGI':
                self.look_word(conned,msg[1],self.log_user)
            elif msg[0]=="QUERY":
                self.qurt(conned,msg[1])
            elif msg[0]=="HIST":
                self.lishichaxun(conned)
        self.sql.sql_cloes()
        conned.close()
    # 用户登录/注册
    def look_word(self,sock:socket,msg:str,zhixing):
        msg=msg.split(" ",1)
        jieguo=self.sql.cahxun(msg)
        print(jieguo)
        zhixing(sock,msg,jieguo)
    # 登录
    def look_user(self,sock,msg,jieguo):
        # 用户名和密码匹配则成功
        if jieguo and jieguo[2] == msg[1]:
            sock.send(b"OK")
            self.userid = jieguo[0]
        else:
            sock.send(b"FAIL")
    # 注册
    def log_user(self,sock,msg:str,jieguo):
        # 判断是否存在用户,存在则返回失败,不存在则表单内插入用户
        if jieguo:
            sock.send(b"FAIL")
        else:
            print("开始插入用户信息")
            # 捕获插入异常，如发生异常回滚
            try:
                date="insert user(name,password) values('%s','%s')"%(msg[0],msg[1])
                print(date)
                self.sql.cur.execute(date)
                self.sql.db.commit()
            except:
                self.sql.db.rollback()
                sock.send(b"FAIL")
            else:
                sock.send(b"OK")
    # 单词查询
    def qurt(self,sock,msg):
        msg = msg.split(" ", 1)
        print(self.userid)
        jieguo=self.sql.chadanci(msg,self.userid)
        if jieguo :
            sock.send(jieguo[2].encode())
        else:
            sock.send(b'FAIL')
    # 历史查询
    def lishichaxun(self,sock):
        date=self.sql.chalishi(self.userid)
        x=1
        for word,mean,times in date:
            value=("%s: %s %s %s")%(x,word,mean,times)
            x+=1
            sock.send(value.encode())
            time.sleep(0.01)
        sock.send(b"##")
class Mysql:
    def __init__(self):
        self.host='127.0.0.1'
        self.port=3306
        self.user='root'
        self.password='123456'
        self.database='python'
        self.charset="utf8"
        self.connet()
    def connet(self):
        addr={
            'host':self.host,
            'port':self.port,
            'user':self.user,
            'password':self.password,
            'database':self.database,
            'charset':self.charset
        }
        self.db=pymysql.connect(**addr)
        self.cur=self.db.cursor()
        print("链接数据库成功")
    def sql_cloes(self):
        self.db.close()
        self.cur.close()
    # 数据库查询用户是否存在
    def cahxun(self,msg):
        date="select id,name,password from user where name='%s';"%msg[0]
        self.cur.execute(date)
        jieguo=self.cur.fetchone()
        return jieguo
    # 查询数据表内单词解释，并把记录插入到历史记录表格。
    def chadanci(self,msg,userid):
        date = "select * from dict where word='%s';" % msg[1]
        print(date)
        self.cur.execute(date)
        jieguo = self.cur.fetchone()
        mytime = time.strftime("%Y/%m/%d %H:%M:%S")
        self.charu(jieguo,userid,mytime)
        return jieguo

    def charu(self,jieguo,userid,mytime):
        if jieguo:
            charu = "insert into user_query(user_id,dict_id,time) values (%s,%s,'%s')" % (userid, jieguo[0], mytime)
        else:
            charu = "insert into user_query(user_id,dict_id,time) values (%s,%s,'%s')" % (userid,'NULL', mytime)
        try:
            self.cur.execute(charu)
            self.db.commit()
        except:
            self.db.rollback()
            print('出错了')
    # 根据用户id 查询历史记录表
    def chalishi(self,userid):
        data='select word,mean,time from user_query as qu left join user as us on qu.user_id=us.id left join dict as dic on qu.dict_id=dic.id where user_id=%s limit 10'%userid
        self.cur.execute(data)
        return self.cur.fetchall()
# 自定义线程类
class MyThreaing(Thread):
    def __init__(self,date):
        self.date=date
        self.taget=Word()
        super().__init__()
    def run(self) -> None:
        self.taget.taget(self.date)
# 创建TCP网络连接类
class TcpNetWord:
    def __init__(self,post=8888,url="0.0.0.0"):
        self.post=post
        self.url=url
        self.addr=(url,post)
        self.sock=self.connect()
    def connect(self):
        sock=socket()
        sock.bind(self.addr)
        return sock

    def main(self):
        self.sock.listen(5)
        while True:
            conned,addr=self.sock.accept()
            t=MyThreaing(conned)
            t.start()

if __name__ == '__main__':
    tcpnetword=TcpNetWord()
    tcpnetword.main()