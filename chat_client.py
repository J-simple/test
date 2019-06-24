from socket import *
import sys,os

def do_send(s,name,addr):
	while True:
		w = input('发送:')
		if w.strip() == 'quit':
			msg = 'q ' + name
			s.sendto(msg.encode(),addr)
			sys.exit('退出聊天')

		msg = 'c %s %s'%(name,w)
		s.sendto(msg.encode(),addr)

def do_recv(s):
	while True:
		data,addr = s.recvfrom(2048)
		if data.decode() == 'bye':
			sys.exit(0)
		print(data.decode(),'\n发言：',end = '')
#客户登录,创建套接字，创建子进程(用于聊天消息收发)
def main():
	#获取命令行地址
	if len(sys.argv) < 3:
		print('请输入正确的地址信息')
	Host = sys.argv[1] 
	Port = int(sys.argv[2]) 
	ADDR = (Host,Port)
	s = socket(AF_INET,SOCK_DGRAM) #t此处套接字用于单进程登录
	
	while True:
		name = input('请输入用户名：')
		if not name:
			break
		#与服务器约定姓名以这种形式发送则认为是登录请求
		msg = 'L ' + name
		#发送登录请求
		s.sendto(msg.encode(),ADDR)

		data,addr = s.recvfrom(1024)
		#约定当服务器回复‘ok’表示登录成功
		if data.decode() == 'ok':
			print('您已经进入聊天室')
			#登录成功则退出循环
			break
		#登录失败则循环登录直到成功为止
		else:
			print(data.decode())
	
	pid = os.fork() #注意：进程用于随意收发聊天信息
	if pid < 0:
		print('create process failed',os._exit(0))
	elif pid == 0:
		do_send(s,name,ADDR)
	else:
		do_recv(s)

if __name__ == '__main__':
	main()
'''你好，世界'''