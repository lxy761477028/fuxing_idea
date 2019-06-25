#!/usr/bin/python3
#-*- coding: utf-8 -*-
import paramiko
from stat import S_ISDIR
import os
#paramiko.util.log_to_file('/tmp/sshout')

def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        # stdin.write("Y") #interact with server, typing Y
        print(stdout.read())
        # for x in stdout.readlines():
        # print x.strip("n")
        print('%s OK\n'%(ip))
        ssh.close()
    except :
        print('%s Error\n' %(ip))


# ------获取远端linux主机上指定目录及其子目录下的所有文件------
def __get_all_files_in_remote_dir(sftp, remote_dir):
    # 保存所有文件的列表
    all_files = list()

    # 去掉路径字符串最后的字符'/'，如果有的话
    if remote_dir[-1] == '/':
        remote_dir = remote_dir[0:-1]

    # 获取当前指定目录下的所有目录及文件，包含属性值
    files = sftp.listdir_attr(remote_dir)
    for x in files:
        # remote_dir目录中每一个文件或目录的完整路径
        filename = remote_dir + '/' + x.filename
        # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
        if S_ISDIR(x.st_mode):
            all_files.extend(__get_all_files_in_remote_dir(sftp, filename))
        else:
            all_files.append(filename)
    return all_files



def scp(ip,username,passwd,ssh_path,local_dir):
    # 建立一个加密的管道
    scp = paramiko.Transport((ip, 22))
    # 建立连接
    scp.connect(username=username, password=passwd)
    # 建立一个sftp客户端对象，通过ssh transport操作远程文件
    sftp = paramiko.SFTPClient.from_transport(scp)
    # ssh_path = r"/root/222"
    # local_dir = r'E:\fuxing_idea\SCP'

    all_list = __get_all_files_in_remote_dir(sftp, ssh_path)
    print(all_list)
    for x in all_list:
        all_dir = x.split('/')
        if len(all_dir) == 4:
            sftp.get(str('%s' % x), str(r'%s'% local_dir))
        else:
            for i in range(3,len(all_dir) - 1):
                dir_list = x.split('/', 3)
                all_dir_path = dir_list[3].split('/')
                all_dir_path.pop(-1)
                make_dir = '/'.join(all_dir_path)
                local_dir = os.path.join(local_dir, make_dir)
                print(local_dir)
                if not os.path.exists(local_dir):
                    os.makedirs(r'%s' % local_dir)
                    path_and_filename = os.path.join(local_dir, mak_dir[3])
                    sftp.get(str('%s' % x), str(r'%s' % path_and_filename))
                else:
                    path_and_filename = os.path.join(local_dir, mak_dir[3])
                    sftp.get(str('%s' % x), str(r'%s' % path_and_filename))
    scp.close()

# ssh2("47.96.23.31","root","8#gez11b3a123456","ls")
ssh_path = r"/root/222"
local_dir = r'E:\fuxing_idea\SCP'

scp("47.96.23.31","root","8#gez11b3a123456", ssh_path, local_dir)