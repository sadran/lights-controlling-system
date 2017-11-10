import socket
from threading import Thread
from signal import signal, SIGINT
import os
import shutil

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 1027)
print('Server: starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming connections
sock.listen()
#golbal variable
threads_count = 0
root="/home/ali/Desktop/root/"
share=root+'share/'

def response(connection):
    global threads_count
    threads_count += 1
    print('Server: Thread {}: started.'.format(threads_count))
    try:
        request = connection.recv(4096).decode('ascii').split('\\n')
        print(request)	
        while True:
        	try:
        		func,username,password=request[0].split(':')
        		request.pop(0)
        		logged=login_level(func,username,password)
        	except:
        		#print('no command')
        		continue
        	if logged:
        		print('logged')
        		break

        while True:
        	request += connection.recv(4096).decode('ascii')
       		try:
       			args=request[0].split(':')
       			request.pop(0)
       		except:
       			continue
       		out=user_level(args,username)
       		if out:
       			break
    finally:
        connection.close()
        print('Server: Thread {}: finished'.format(threads_count))
#get msg_id and return message to client
def message(msg_id,path,data):
	print("printing msg: "+str(msg_id))
	#print("data: "+data)
	#print("path: "+path)
	a={ 1 : "Error: You have to log in first!",
	2 : "Ok: User created.",
	3 : "Error: Username exist!",
	4 : "Ok: User removed.",
	5 : "Error: Username or password is wrong!",
	6 :"Ok: User login was successful.",
	7 :"Ok: User logout was successful.",
	8 :"Ok: "+path+".",
	9 :"Error: Wrong path!",
	10:"Ok: File created.",
	11:"Error: File exist!",
	12:"Ok: File removed.",
	13:"Error: No file with that name exist!",
	14:"Ok: File renamed.",
	15:"Ok: File shared.",
	16:"Error: No user with that username exist!",
	17:"Ok: File unshared.",
	18:"Error: File was not shared!",
	19:"Ok: "+data+'.',
	20:"Ok: Data wrote.",
	21:"Ok: File moved.",
	22:"Ok: File copied.",
	23:"Ok: Directory created.",
	24:"Error: Directory exist!",
	25:"Ok: Directory removed.",
	26:"Error: No directory with that name exist!",
	27:"Ok: Directory renamed.",
	#28:"Ok: "+os.listdir(path)+'.',
	29:"Ok: Directory shared.",
	30:"Ok: Directory unshared.",
	31:"Error: Directory was not shared!",
	32:"Ok: Directory moved.",
	33:"Ok: Directory copied.",
	34:"Error: You don’t have permission to change the name!",
	35:"Error: Index out of range!"}
	msg =a.get(msg_id)
	print (msg)
	sock.sendall(msg)
#handel account requests
def login_level(func,username,password):
	userpath=os.path.join(root,username)
	#new-account
	if func == 'new-account':
		if(os.path.isdir(userpath) == False):
			os.mkdir(userpath)
			with open(os.path.join(root)+username+'.txt','w') as f:
				f.write(password) 
				os.chdir(userpath)
				print(os.getcwd())
				message(2,'','')
				return True
		
		else:
			message(3,'','')
			return False

	#rem-account
	elif func == 'rem-account':
		if(os.path.isdir(userpath)):
			with open(os.path.join(root)+username+'.txt','r') as f:
				passw=f.readline()
				if(passw == password):
					os.rmdir(userpath)
					os.remove(os.path.join(root)+username+'.txt')
					message(4,'','')
					return False
		else:
			message(5,'','')
			return False

	#login
	elif func == 'login':
		if(os.path.isdir(userpath)):
			with open(os.path.join(root)+username+'.txt','r') as f:
				passw=f.readline()
				if(passw == password):
					message(6,'','')
					os.chdir(userpath)
					return True
		else:
			message(5,'','')
			return False
	#not permitted to login
	else:
		message(1,'','')
		return False
	#return True
#handle user_mode requests
def user_level(args,username):
	userpath=root+username
	func = args[0]
	print('func: '+func)
	try:
		newpath=userpath+path_builder(args[1],username)
		#print ('newpath: '+newpath)
	except:
		#print("args[1] not found")
		pass
	try:
		target_path=newpath+path_builder(args[2],username)
		#print('target_path: '+target_path)
	except:
		#print("args[2] not found")
		pass
	try:
		file_name=args[2]
	except:
		pass
	try:
		data_arg=args[3]
	except:
		pass
	try:
		tar_path=newpath+path_builder(args[4],username)
	except:
		pass
	#where-am-i
	out = False
	if func == 'where-am-i':
		message(8,os.getcwd(),'')
	#goto
	elif func == 'goto':
		#print('newpath: '+newpath)
		if os.path.isdir(newpath):
			os.chdir(newpath)
			message(8,newpath,'')
		else:
			message(9,'','')

	#working with dir
	#new-dir
	elif func == 'new-dir':
		#print("userpath: "+userpath)
		#print("newpath: "+newpath)
		#print("target_path: "+target_path)
		if(os.path.isdir(newpath)):
			if not os.path.isdir(target_path):
				os.mkdir(target_path)
				message(23,'','')
			else:
				message(24,'','')
		else:
			message(9,'','')
	#rem-dir
	elif func == 'rem-dir':
		if(os.path.isdir(newpath)):
			if os.path.isdir(target_path):
				shutil.rmtree(target_path)
				message(25,'','')
			else:
				message(26,'','')
		else:
			message(9,'','')
	#ls-dir
	elif func == 'ls-dir':
		if(os.path.isdir(newpath)):
			if os.path.isdir(target_path):
				message(28,target_path,'')
			else:
				message(26,'','')
		else:
			message(9,'','')	
	#mv-dir
	elif func == 'mv-dir':
		if os.path.isdir(newpath) and os.path.isdir(tar_path):
			print(target_path)
			if os.path.isdir(target_path):
				dest_path=userpath+path_builder(args[3],username)+path_builder(args[4],username)
				#print('dest_path: '+dest_path)
				if not os.path.isdir(dest_path):
					shutil.move(target_path,dest_path)
					message(32,'','')
				else:
					message(24,'','')
			else:
				message(26,'','')
		else:
			message(9,'', '')
	#cp-dir
	elif func == 'cp-dir':
		if os.path.isdir(newpath) and os.path.isdir(tar_path):
			print(target_path)
			if os.path.isdir(target_path):
				dest_path=userpath+path_builder(args[3],username)+path_builder(args[4],username)
				print('dest_path: '+dest_path)
				if not os.path.isdir(dest_path):
					shutil.copytree(target_path,dest_path)
					message(32,'','')
				else:
					message(24,'','')
			else:
				message(26,'','')
		else:
			message(9,'', '')
	#share-dir
	elif func == 'share-dir':
		if os.path.isdir(newpath):
			print('target_path: '+target_path)
			if os.path.isdir(target_path):
				dest_path=root+args[3]+'/'+path_builder(args[2],username)
				print('dest_path: '+dest_path)
				if not os.path.isdir(dest_path):
					if not os.path.isdir(dest_path):
						os.symlink(target_path,dest_path)
						with open(share+args[2]+'+'+username,'a+') as txt:
							txt.write(args[3])
						message(29,'','')
					else:
						message(24,'','')
				else:
					message(16,'','')
			else:
				message(26,'','')
		else:
			message(9,'','')
	#unshare-dir
	elif func == 'unshare-dir':
		print('unshare')
		share_dir=root+args[3]
		dir_name=args[3]
		if os.path.isdir(newpath):
			print('target_path: '+target_path)
			if os.path.isdir(target_path):
				print('share-dir: '+share_dir)
				if os.path.isdir(share_dir):
					print('share-file: '+share+args[2]+'+'+username)
					with open(share+args[2]+'+'+username,'a+') as txt:
						txt.seek(0)
						names=txt.read().split('\n')
						print(names)
						if dir_name in names:
							print(dir_name)
							names.remove(dir_name)
							print(names)
							txt.truncate()
							txt.write('\n'.join(names))
							if rmlink(root+args[3]+'/',path_builder(args[2],username)):
								message(30,'','')
							else:
								message(31,'','')
						else:
							message(31,'','')
				else:
					message(16,'','')
			else:
				message(26,'','')
		else:
			message(9,'','')
	#share-dir
	elif func == 'ren-dir':
		ren_path=newpath+'/'+args[3]
		if os.path.isdir(newpath):
			print(target_path)
			if os.path.isdir(target_path):
				if not os.path.isdir(ren_path):
					if isshared(target_path,username):
						os.rename(target_path,ren_path)
						message(14,'','')
					else:
						message(34,'','')
				else:
					message(24,'','')
			else:
				message(26,'','')
		else:
			message(9,'','')
	#working with file
	#new-file
	elif func == 'new-file':
		print('here!')
		if os.path.isdir(newpath):
			print(newpath)
			if not os.path.isfile(target_path):
				print(target_path)
				with open(target_path,'w+') as f:
					pass
				message(12,'','')
			else:
				message(11,'','')
		else:
			message(9,'','')
	#rem-file
	elif func == 'rem-file':
		if os.path.isdir(newpath):
			if  os.path.isfile(target_path):
				os.remove(target_path)
				message(12,'','')
			else:
				message(11,'','')
		else:
			message(9,'','')
	#mv-file
	elif func == 'mv-file':
		if os.path.isdir(newpath) and os.path.isdir(tar_path):
			print(target_path)
			if os.path.isfile(target_path):
				dest_path=userpath+path_builder(args[3],username)+path_builder(args[4],username)
				print('dest_path: '+dest_path)
				if not os.path.isfile(dest_path):
					shutil.move(target_path,dest_path)
					message(21,'','')
				else:
					message(11,'','')
			else:
				message(13,'','')
		else:
			message(9,'', '')
	#cp-file
	elif func == 'cp-file':
		if os.path.isdir(newpath) and os.path.isdir(tar_path):
			print(target_path)
			if os.path.isfile(target_path):
				dest_path=userpath+path_builder(args[3],username)+path_builder(args[4],username)
				print('dest_path: '+dest_path)
				if not os.path.isfile(dest_path):
					shutil.copyfile(target_path,dest_path)
					message(21,'','')
				else:
					message(11,'','')
			else:
				message(13,'','')
		else:
			message(9,'', '')
	#read-file
	elif func == 'read-file':
		if os.path.isdir(newpath):
			if os.path.isfile(target_path):
				with open(target_path,'r') as file:
					data=file.read()
					message(19,'',data)
			else:
				message(13,'','')
		else:
			message(9,'','')
	#write-file
	elif func == 'write-file':
		if os.path.isdir(newpath):
			if os.path.isfile(target_path):
				with open(target_path,'w') as file:
					file.write(data_arg)
					message(20,'','')
			else:
				message(13,'','')
		else:
			message(9,'','')
	#write-char
	elif func == 'write-char':
		start=int(args[3])
		end=int(args[4])
		data_arg=args[5]
		#print(len(data_arg))
		if os.path.isdir(newpath):
			if os.path.isfile(target_path):
				with open(target_path,'r+') as file:
					tar_size=len(file.read())
					#print('tar_size: '+str(tar_size))
					if start in range(tar_size-len(data_arg)) and end == start+len(data_arg):
						file.seek(start)
						file.write(data_arg)
						message(20,'','')
					else:
						message(35,'','')
			else:
				message(13,'','')
		else:
			message(9,'','')
	#share-file
	elif func == 'share-file':
		if os.path.isdir(newpath):
			print('target_path: '+target_path)
			if os.path.isdir(target_path):
				dest_path=root+args[3]+'/'+path_builder(args[2],username)
				print('dest_path: '+dest_path)
				if not os.path.isdir(dest_path):
					if not os.path.isdir(dest_path):
						os.symlink(target_path,dest_path)
						with open(share+args[2]+'+'+username,'a+') as txt:
							txt.write(args[3])
						message(29,'','')
					else:
						message(24,'','')
				else:
					message(16,'','')
			else:
				message(26,'','')
		else:
			message(9,'','')
	#unshare-file
	elif func == 'unshare-file':
		print('unshare')
		share_dir=root+args[3]
		dir_name=args[3]
		if os.path.isdir(newpath):
			print('target_path: '+target_path)
			if os.path.isdir(target_path):
				if os.path.isdir(share_dir):
					with open(share+args[2]+'+'+username,'w+') as txt:
						names=txt.read().split('\n')
						print(names)
						if dir_name in names:
							print(dir_name)
							names.remove(dir_name)
							print(names)
							txt.truncate()
							txt.write('\n'.join(names))
							if rmlink(root+args[3]+'/',path_builder(args[2],username)):
								message(30,'','')
							else:
								message(31,'','')
						else:
							message(31,'','')
				else:
					message(16,'','')
			else:
				message(26,'','')
		else:
			message(9,'','')
	#ren-file
	elif func == 'ren-file':
		ren_path=newpath+'/'+args[3]
		if os.path.isdir(newpath):
			print(target_path)
			if os.path.isfile(target_path):
				if not os.path.isfile(ren_path):
					if not isshared(target_path,username):
						os.rename(target_path,ren_path)
						message(14,'','')
					else:
						message(34,'','')
				else:
					message(24,'','')
			else:
				message(26,'','')
		else:
			message(9,'','')

	#logout
	elif func == 'logout':
		out=True
		message(7,'','')
	#not command
	else:
		print("Error:dare chert o pert mifereste!")

	return out
#make symbolink
def link(src,dest):
	print('create link!')
	#print(os.listdir(src))
	#filenames=[f for f in os.listdir(src) if os.path.isfile(os.path.join(src,f))]
	#print(filenames)
	#dirnames=[f for f in os.listdir(src) if os.path.isdir(os.path.join(src,f))]
	#print(dirnames)
	#print('src: '+src)
	os.symlink(src,dest)
	#shutil.rmtree(dest+'/')
	#print(os.listdir(dest))
	#for file in filenames:
	#	print('file: '+file)
	#	os.symlink(os.path.join(src,file),os.path.join(dest,file))
	#for dirname in dirnames:
	#	print('dirname: '+dirname)
	#	link(os.path.join(src,dirname),os.path.join(dest,dirname))
def path_builder(path,username):
	#elemanes=path.split('/')
	#new_elemane=''
	#for elemane in elemanes:
	#	if elemane != '':
	#		new_elemane+=elemane+'+'+username+'/'
	#	else:
	#		new_elemane+='/'
	#return new_elemane[:-1]
	return path
def rmlink(src,name):
	print('in rmlink: src='+src)
	ls=os.listdir(src)
	dirs=[f for f in os.listdir(src) if os.path.isdir(os.path.join(src,f))]
	for obj in ls:
		if obj == name:
			print('src+obj: '+src+obj)
			os.remove(src+obj)
			return True
	for obj in dirs:
		if rmlink(src+obj+'/',name):
			return True
	return False
def isshared(src,username):
	tar_name=src.split('/')[-1]
	names=os.listdir(src)
	for name in names:
		if name.split('+')[:-1] == tar_name and name.split('+')[-1] != username:
			return True
	return False



while True:
    # Wait for a connection
    print('Server: waiting for a connection')
    connection, client_address = sock.accept()
    Thread(target=response, args=(connection,)).start()

