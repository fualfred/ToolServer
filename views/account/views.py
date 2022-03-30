# !/usr/bin/python
# -*-coding:utf-8-*-
from flask import Blueprint, request, jsonify
from utils.db_pool import get_connection, close

account_blue = Blueprint('account', __name__, url_prefix='/api')


@account_blue.route("/addAccount", methods=['POST'])
def create_account():
    request_data = request.get_json()
    first_name = request_data.get('first_name')
    last_name = request_data.get('last_name')
    email = request_data.get('email')
    password = "$2a$12$19qQKiHGrTieBqBztJUK3OUcZHNPr78G5kqBf29ilIK/hp8ck..y6"

    sql = 'insert into b_account(first_name,last_name,password,email,should_change_psw_flag,email_verified_flag,installer_flag) VALUES("%s","%s","%s","%s",%s,%s,%s);' % (
        first_name, last_name, password, email, 0, 1, 1)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        close(conn, cursor)
        return jsonify({"code": 0, "msg": "账号创建成功"})
    except Exception as e:
        close(conn, cursor)
        return jsonify({"code": 1, "msg": "账号创建失败", "errorMsg": str(e)})


@account_blue.route("/queryAccount", methods=['GET'])
def query_account():
    email = request.args.get('email')
    sql = 'select id from b_account where email="%s";' % email
    print(sql)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        close(conn, cursor)
        if len(result) == 0:
            return jsonify({"code": 0, "msg": "该邮箱未注册，可正常使用", "result": result})
        else:
            return jsonify({"code": 0, "msg": "该邮箱已注册，不可使用", "result": result})
    except Exception as e:
        close(conn, cursor)
        return jsonify({"code": 1, "msg": "查询失败", "errorMsg": str(e)})
