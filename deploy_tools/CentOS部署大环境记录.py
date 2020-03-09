import os
from fabric import Connection
from time import sleep
#CentOS7外网已连接部署。
# # 设置网络参数
# nmcli connection add type bond con-name bond0 ifname bond0
# nmcli connection modify bond0 mode balance-alb
# nmcli connection modify bond0 ipv4.method manual
# nmcli connection modify bond0 ipv4.addresses 10.24.1.221/24
# nmcli connection modify bond0 ipv4.gateway 10.24.1.2
# nmcli connection modify bond0 autoconnect yes
# #添加并启动两张从网卡

# nmcli connection add type bond-slave ifname enp2s0f0  master bond0
# nmcli connection add type bond-slave ifname enp2s0f1  master bond0
# nmcli connection up bond-slave-enp2s0f0
# nmcli connection up bond-slave-enp2s0f1
# #查看bond状态
# cat /proc/net/bonding/bond0

def put_file(filename,conn):
    '''
    放同名文件
    '''
    conn.put(filename,filename)


def pip3_local_install(user,mod,mod_dir):
    '''
    用pip3本地文件夹离线安装，user安装的用户，mod模块名，mod_dir模块离线包目录
    安装完成后删除文件夹
    '''
    if user=='root':
        conn.run('pip3 install '+mod+' --no-index --find-links=file:///'+user+'/'+mod_dir)
        conn.run('rm -rf '+'/'+user+'/'+mod_dir)
    else:
        conn.run('pip3 install '+mod+' --no-index --find-links=file:///home'+'/'+user+'/'+mod_dir)
        conn.run('rm -rf '+'/home'+'/'+user+'/'+mod_dir)
    


def excute_any(command,conn):
    '''
    执行命令即使知道会返回错误
    '''
    try:
        conn.run(command)      #解决错误通过find / -name "*libcap.so*"找到文件/usr/bin/ld: cannot find -lcap
    except:pass


def sed_on_vsftpd_config(newtext,newtext_value,conn,filepath='/etc/vsftpd/vsftpd.conf'):
    if not newtext+'=' in conn.run('cat '+filepath+' | grep -v "#"').stdout:
        conn.run("sed -i '$a "+newtext+'='+newtext_value+"' "+filepath)
    try:
        next_grep=conn.run('cat '+filepath+' | grep -v "#" | grep "'+newtext+'='+newtext_value+'"').stdout
    except:
        next_grep=''
    if not newtext+'='+newtext_value in next_grep: 
        conn.run("sed -i 's/"+newtext+r'.*'+"/"+newtext+'='+newtext_value+"/g' "+filepath)


def make_file_upload_and_delete(filename,strdd,target_filename,conn):
    '''
    打开临时文件，写完支行上传到服务器。
    '''
    with open(filename,'wb') as f:
        f.write(strdd.encode())
    conn.put(filename,target_filename)
    os.remove(filename)




host='175.24.111.140'
user='root'
password='Dan;06623QQ'
hostname='DDWebHost'
web_user='django_dd'
web_user_pass='Dan;06623'
dd_sudo='sudo -u '+web_user+' '

conn=Connection(host, user=user,connect_kwargs={"password": password})
conn.run('ls -a')





conn.run('hostname '+hostname)    #修改主机名称

# #配置yum使用环境
# #需要先将光盘内容复制到机器
# #些本地repo文件，并移除系统文件

# strdd='''[dd_local_yum]
# name=dd_local_yum
# baseurl=file:////home/dd/CentOS8.1_ISO/AppStream
# enabled=1
# gpgcheck=0
# '''
# with conn.cd('/etc/yum.repos.d/'):
    # conn.run('mkdir -p backups')
    # excute_any('mv Cent* backups',conn)
    # make_file_upload_and_delete('bb.repo',strdd,'/etc/yum.repos.d/bb.repo',conn)

# strdd='''[Base_local_yum]
# name=Base_local_yum
# baseurl=file:////home/dd/CentOS8.1_ISO/BaseOS
# enabled=1
# gpgcheck=0
# '''
# with conn.cd('/etc/yum.repos.d/'):
    # make_file_upload_and_delete('BaseOS_local.repo',strdd,'/etc/yum.repos.d/BaseOS_local.repo',conn)

# conn.run('yum clean all')    #清除资源，可以发现yum错误。
# conn.run('yum makecache')    #建立yum资源缓存




#升级sqlite3配置

put_file('sqlite-autoconf-3310100.tar.gz',conn)
conn.run('mv sqlite-autoconf-3310100.tar.gz /usr/local/src/')
with conn.cd('/usr/local/src/'):
    conn.run('tar -xvf sqlite-autoconf-3310100.tar.gz')
    with conn.cd('sqlite-autoconf-3310100/'):
        conn.run('./configure --prefix=/usr/local')
        conn.run('make && make install')
conn.run('rm -rf /usr/local/src/sqlite-autoconf-3310100/')
excute_any('mv /usr/bin/sqlite3  /usr/bin/sqlite3_old',conn)
excute_any('ln -s /usr/local/bin/sqlite3   /usr/bin/sqlite3',conn)    #软链接将新的sqlite3设置到/usr/bin目录下
#添加开机启动

sqlite3_add_str='export LD_LIBRARY_PATH="/usr/local/lib"'
if not sqlite3_add_str in conn.run('cat .bashrc').stdout:
    strdd=conn.run('cat .bashrc').stdout+f'\n{sqlite3_add_str}\n'
    make_file_upload_and_delete('.bashrc',strdd,'.bashrc',conn)
conn.run('export LD_LIBRARY_PATH="/usr/local/lib"')
conn.run('source .bashrc')




#将Python源码包tar、getpip.py放入sftp放入服务器。
put_file('get-pip.py',conn)
put_file('Python-3.8.1.tar.xz',conn)

if conn.is_connected:
    conn.run('ls -a')

# 先安装pip和Python3运行环境


conn.run('yum install libffi libffi-devel -y')    #ctype错误，pip需要
conn.run('yum install readline readline-devel  -y')    #让python可以用上下左右箭头
conn.run('yum install openssl openssl-devel -y')    #fabric需要
conn.run('yum install  openssl-devel -y')    #fabric需要



#安装Python3.8.1和pip3

conn.run('mv Python-3.8.1.tar.xz /usr/local/src/')
with conn.cd('/usr/local/src/'):
    conn.run('tar -xvf Python-3.8.1.tar.xz')
    with conn.cd('Python-3.8.1/'):
        conn.run('./configure')
        conn.run('make')
        excute_any('make test',conn)
        conn.run('make install')
conn.run('rm -rf /usr/local/src/Python-3.8.1/')




#更改pip3源
strdd='''[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
'''

conn.run("mkdir -p /root/.pip/")
conn.run("mkdir -p /root/.pip3/")
make_file_upload_and_delete('pip.conf',strdd,'/root/.pip/pip.conf',conn)
make_file_upload_and_delete('pip3.conf',strdd,'/root/.pip3/pip3.conf',conn)
conn.run('pip3 install --upgrade pip')



#安装fabric


put_file('fabric-linux-CentOS.zip',conn)
conn.run('unzip fabric-linux-CentOS.zip')
pip3_local_install(user,'fabric','fabric-linux-CentOS')





#安装virtualenv


put_file('virtualenv-linux-CentOS.zip',conn)
conn.run('unzip virtualenv-linux-CentOS.zip')
pip3_local_install(user,'virtualenv','virtualenv-linux-CentOS')




# #源码方式安装并配置vsftpd


# put_file('vsftpd-3.0.3.tar.gz',conn)
# conn.run('tar -xvf vsftpd-3.0.3.tar.gz')
# # 新建配置目录1

# conn.run('mkdir -p /etc/vsftpd')
# with conn.cd('vsftpd-3.0.3'):
    # # 如需要tcp wrapper，改成#define VSF_BUILD_TCPWRAPPERS
    # # 如需要OpenSSL，改成#define VSF_BUILD_SSL
    # # 建议吧所有的undef改为define，反正也不多，就三四个。
    # # 改完直接make即可。
    
    # conn.run('sed -i "s/^#undef VSF_BUILD_TCPWRAPPERS.*/#define VSF_BUILD_TCPWRAPPERS/g" builddefs.h')
    # conn.run('sed -i "s/^#undef VSF_BUILD_SSL.*/#define VSF_BUILD_SSL/g" builddefs.h')
    # #编译前环境配置
    
    # conn.run('yum install tcp_wrappers-devel -y')
    # conn.run('yum install openssl-devel -y')
    # conn.run('yum install pam-devel -y')
    # conn.run('yum install libcap -y')
    # with conn.cd('/usr/lib'):
        # excute_any('ln -s /usr/lib64/libcap.so.2 libcap.so',conn)      #解决错误通过find / -name "*libcap.so*"找到文件/usr/bin/ld: cannot find -lcap
    # conn.run('make')
    # excute_any('useradd nobody',conn)    #需要配置nobody用户防止没有
    # conn.run('mkdir -p /usr/share/empty/')    #需要配置空文件夹防止没有
    # #配置anonymous FTP
    
    # conn.run('mkdir -p /var/ftp/')
    # excute_any('useradd -d /var/ftp ftp',conn)
    # conn.run('chown root:root /var/ftp')
    # conn.run('chmod og-w /var/ftp')
    # #安装bin文件
    
    # conn.run('mkdir -p /usr/local/man/man5')
    # conn.run('mkdir -p /usr/local/man/man8')
    # conn.run('make install')
    # # excute_any('cp vsftpd /usr/local/sbin/vsftpd',conn)
    # excute_any('cp vsftpd.conf /etc/vsftpd/vsftpd.conf',conn)    #源码的配置文件cp到配置目录




#yum安装并配置vsftpd


conn.run('yum install vsftpd -y')
# 修改/etc/vsftpd/vsftpd.conf 

# 让本地时间取代GMT时间

sed_on_vsftpd_config('use_localtime','YES',conn)
# 关闭anonymous访问

sed_on_vsftpd_config('anonymous_enable','NO',conn)
# 开启禁止访问用户列表，使只有表中的人才可使用ftp

sed_on_vsftpd_config('userlist_enable','YES',conn)
sed_on_vsftpd_config('userlist_deny','NO',conn)
sed_on_vsftpd_config('userlist_file','/etc/vsftpd/user_list',conn)
strdd='''dd
ylkj
yl
'''
make_file_upload_and_delete('user_list',strdd,'/etc/vsftpd/user_list',conn)
# 开启欢迎信息,并将欢迎信息写入文件。

sed_on_vsftpd_config('banner_file','/etc/vsftpd/welcom.txt',conn)
strdd='''Welcom to CAYL_XXKJ
欢迎来到榆林分行信息科技部维护人员用ftp
-----------------------------------
说明：
Drivers：各种设备的驱动
ManySystems：各种系统安装文件
Images：主机系统镜像
RemoteInstall：远程安装需要的工具
'''
make_file_upload_and_delete('welcom.txt',strdd,'/etc/vsftpd/welcom.txt',conn)

#开启上传功能

sed_on_vsftpd_config('write_enable','YES',conn)
sed_on_vsftpd_config('local_umask','002',conn) 
# 开启实体用户chroot，使所有用户不可跳转出home自身的目录。
#添加例外列表可以使最高管理员切换(最高管理员添加为dd)

sed_on_vsftpd_config('chroot_local_user','YES',conn)
sed_on_vsftpd_config('allow_writeable_chroot','YES',conn)    #防止不可进入有写权限的chroot目录
sed_on_vsftpd_config('chroot_list_enable','YES',conn)
sed_on_vsftpd_config('chroot_list_file','/etc/vsftpd/chroot_list',conn)
#没例外账户也得添加文件

with open('chroot_list','wb') as f:
    str_dd='dd\n'.encode()
    f.write(str_dd)
conn.put('chroot_list','/etc/vsftpd/chroot_list')
os.remove('chroot_list')
#管理员添加为ylkj,普通人员为yl并配置相关目录权限
#ylkj可以修改文件，而yl只可以读

excute_any('useradd -g ftp -d /home/ylkj_ftp ylkj',conn)
excute_any('usermod -s /bin/bash ylkj',conn)    #不能使ftp用户无法登陆系统
conn.run("echo 'ylkj:Yl123456.' | chpasswd")
conn.run("chmod g=rwx,o=rx /home/ylkj_ftp")
excute_any('useradd -g ftp -d /home/ylkj_ftp/yl_ftp yl',conn)
excute_any('usermod -s /bin/bash yl',conn)    #使ftp用户无法登陆系统
conn.run("echo 'yl:123123' | chpasswd")
conn.run("chmod u=rx,g=rwx,o=rx /home/ylkj_ftp/yl_ftp")
#限制最大同时上线人数，每个IP最多使用一条数据连接

sed_on_vsftpd_config('max_clients','45',conn)
sed_on_vsftpd_config('max_per_ip','5',conn)
#增加ssl到ftp增加安全性。暂时关闭，无法使用
#先制作pem证书 cd /etc/pki/tls/certs
#make vsftpd.pem && cp vsftpd.pem /etc/vsftpd

sed_on_vsftpd_config('ssl_enable','NO',conn)
sed_on_vsftpd_config('allow_anon_ssl','NO',conn)    #不容许匿名用户使用验证证书
sed_on_vsftpd_config('force_local_data_ssl','NO',conn)
sed_on_vsftpd_config('force_local_logins_ssl','NO',conn)
sed_on_vsftpd_config('ssl_tlsv1','NO',conn)
sed_on_vsftpd_config('ssl_sslv2','NO',conn)
sed_on_vsftpd_config('ssl_sslv3','NO',conn)

conn.run('systemctl enable vsftpd')
conn.run('systemctl restart vsftpd')
#开放防火墙给ftp

# conn.run('firewall-cmd --add-service=ftp --permanent')
# conn.run('firewall-cmd --reload')




#修改时区并配置NTP服务器
conn.run('yum install ntpdate -y')
conn.run('timedatectl set-timezone Asia/Shanghai')
conn.run('timedatectl set-ntp yes')
conn.run('timedatectl set-local-rtc 1')
excute_any('ntpdate 10.24.252.250',conn)      #和下联区电信路由同步
excute_any('ntpdate 10.24.252.252',conn)      #和核心区SW1同步
excute_any('ntpdate 10.24.1.221',conn)      #和核心区ftp服务器同步
excute_any('ntpdate cn.ntp.org.cn',conn)      #和外网服务器同步

conn.run('yum install chrony -y')
strdd='''# Use public servers from the pool.ntp.org project.
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
server 10.24.252.250 iburst
server 10.24.252.252 iburst
server cn.ntp.org.cn iburst

# Record the rate at which the system clock gains/losses time.
driftfile /var/lib/chrony/drift

# Allow the system clock to be stepped in the first three updates
# if its offset is larger than 1 second.
makestep 1.0 3

# Enable kernel synchronization of the real-time clock (RTC).
rtcsync

# Enable hardware timestamping on all interfaces that support it.
#hwtimestamp *

# Increase the minimum number of selectable sources required to adjust
# the system clock.
#minsources 2

# Allow NTP client access from local network.
allow 192.168.0.0/16
allow 10.24.0.0/16

# Serve time even if not synchronized to a time source.
#local stratum 10

# Specify file containing keys for NTP authentication.
#keyfile /etc/chrony.keys

# Specify directory for log files.
logdir /var/log/chrony

# Select which information is logged.
#log measurements statistics tracking
'''

make_file_upload_and_delete('chrony.conf',strdd,'/etc/chrony.conf',conn)
conn.run('systemctl enable chronyd')
conn.run('systemctl restart chronyd')
#开放防火墙给ntp

# conn.run('firewall-cmd --add-service=ntp --permanent')
# conn.run('firewall-cmd --reload')
# conn.run('cat /etc/vsftpd/vsftpd.conf | grep -v "#"')




#安装django

put_file('django-linux.zip',conn)
conn.run('unzip django-linux.zip')
pip3_local_install(user,'django','django-linux')





#添加web用户

excute_any('useradd  -m '+web_user,conn)
excute_any('usermod -s /bin/bash '+web_user,conn)
excute_any('usermod -G wheel '+web_user,conn)
conn.run("echo '"+web_user+":"+web_user_pass+"' | chpasswd")

if not 'AllowUsers' in conn.run('cat /etc/ssh/sshd_config | grep -v "#"').stdout:
    conn.run(f"sed -i '$a AllowUsers {web_user} {user}' /etc/ssh/sshd_config")
elif not f'AllowUsers {web_user} {user}' in conn.run('cat /etc/ssh/sshd_config | grep -v "#"').stdout:
    conn.run(f"sed -i 's/AllowUsers.*/AllowUsers {web_user} {user}/g' /etc/ssh/sshd_config")

conn.run('systemctl restart sshd')
