# !/usr/bin/python
# -*-coding:utf-8-*-
from flask import Blueprint, request, jsonify, current_app
import os
from utils.ssh_client import get_ssh_client, disconnect

ota_blue = Blueprint('ota', __name__, url_prefix='/api')


@ota_blue.route('/upload', methods=["POST"])
def upload_file():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"code": 1, "msg": "上传文件参数为空"})
        else:
            file.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), file.filename))
            file.close()
            return jsonify({"code": 0, "msg": "上传成功"})
    except Exception as e:
        return jsonify({"code": 2, "msg": "上传失败", "errorMsg": str(e)})


@ota_blue.route('/uploadFileToServer', methods=["POST"])
def upload_file_to_server():
    request_data = request.get_json()
    device_model = request_data.get("device_model")
    firm_name = request_data.get("firmware_name")
    firmware_version = request_data.get("firmware_version")
    file_name = request_data.get("file_name")
    version_code = request_data.get("version_code")
    md5_value = request_data.get("md5")
    try:
        ssh = get_ssh_client()
        mk_dir = r"/root/arizeTestTools/firm" + "/" + device_model + "/" +firm_name
        # print(mk_dir)
        cmd = "mkdir -p "+ mk_dir
        in_put, stdout, stderr = ssh.exec_command(cmd)
        print(in_put, stdout, stderr)
        sftp = ssh.get_transport().open_sftp_client()
        sftp.put(os.path.join(current_app.config.get('UPLOAD_FOLDER'), file_name), mk_dir + '/' + file_name)
        sftp.close()
        disconnect(ssh)
        return jsonify({"code": 0, "msg": "上传文件到服务器成功"})
    except Exception as e:
        sftp.close()
        disconnect(ssh)
        return jsonify({"code": 1, "msg": "上传文件到服务器失败", "errorMsg": str(e)})
