import paramiko
import os
import re
import sys
import msvcrt

username = '*****'
pw1 = '***************'
host_ip_list1 = '192.168.50.130'


def run(host_ip, username, password, command):
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_ip, 22, username, password)
        print('===================exec on [%s]=====================' % host_ip)
        print(ssh.exec_command(command, timeout=300)[1].read().decode('utf-8'))
    except Exception as ex:
        print('error, host is [%s], msg is [%s]' % (host_ip, ex.message))
    finally:
        ssh.close()


if __name__ == '__main__':
    paramiko.util.log_to_file('paramiko.log')
    try:
        while True:
            print('请选择操作类型：1.新增；2.删除；其它健退出')
            s = input()
            if s == '1':
                print('请输入隔离IP')
                line = input()
                if line == '\n':
                    break
                command1 = 'sudo iptables -A INPUT -s ' + line + \
                    ' -j DROP && sudo service iptables save && sudo systemctl restart iptables'

                cmd1 = 'sudo iptables -D INPUT -s '+line + \
                    ' -j DROP'

                '''
                为避免添加策略重复，此处先进行删除已有策略操作
                '''
                run(host_ip_list1, username, pw1, cmd1)
                '''
                添加新策略
                '''
                run(host_ip_list1, username, pw1, command1)

                cmd = 'sudo iptables -L -n |grep '+line
                print('********************确认信息********************')
                run(host_ip_list1, username, pw1, cmd)

                print("执行成功！")
            elif s == '2':
                print('请输入隔离IP')
                line = input()
                if line == '\n':
                    break
                cmd1 = 'sudo iptables -D INPUT -s '+line + \
                    ' -j DROP && sudo service iptables save && sudo systemctl restart iptables'
                run(host_ip_list1, username, pw1, cmd1)

                cmd = 'sudo iptables -L -n |grep '+line
                print('********************确认信息********************')
                run(host_ip_list1, username, pw1, cmd)

                print("执行成功！")
            else:
                sys.exit("goodbye!")
    except Exception as e:
        print(e)
