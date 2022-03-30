# !/usr/bin/python
# -*-coding:utf-8-*-
import paramiko

ssh_config = {
    "hostname": "1xxxxx",
    "port": 22,
    "username": "root",
    "password": "xxxx"
}
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def get_ssh_client():
    try:
        ssh_client.connect(**ssh_config)
        return ssh_client
    except Exception as e:
        print(e)
        return None


def disconnect(client):
    client.close()


print(get_ssh_client())
