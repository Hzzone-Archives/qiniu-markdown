# -*- coding: utf-8 -*-
import qiniu
import json
import os
import getopt
import sys

# init the config and auth
def init():
    cfg = config()
    global access_key
    global secret_key
    global bucket_name
    global domain
    global q
    access_key = cfg["access_key"]
    secret_key = cfg["secret_key"]
    bucket_name = cfg["bucket_name"]
    domain = cfg["domain"]
    # 构建鉴权对象
    q = qiniu.Auth(access_key, secret_key)

def config():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "config.json")):
        print("Config File Not Found in Current Folder")
    f = open("config.json", encoding='utf-8')
    cfg = json.load(f)
    return cfg

# upload and return markdown link
def upload(path):
    if not os.path.exists(path):
        print("%s not exists" % path)

    file_name = os.path.basename(path)
    key = None
    # print(key)
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    ret, info = qiniu.put_file(token, key, path)
    # print(info["text_body"]["key"])
    # print(ret['key'])
    link = "http://"+domain+"/"+ret["key"]
    link = "![](%s)" % link
    # print(link)
    return file_name, link
    # assert ret['key'] == key
    # assert ret['hash'] == qiniu.etag(file_name)

def help():
    print("How to Use")

if __name__ == "__main__":
    init()
    # upload("test.png")
    try:
        options, args = getopt.getopt(sys.argv[1:], "hp:i:", ["help", "ip=", "port="])
    except getopt.GetoptError:
        sys.exit()

    if len(args)>1:
        print("Param is no more than 1")
        exit(0)
    elif len(args)==1:
        pass
    else:
        print("See -h or --helpe for user instruction")
    # upload one image
    path = args[0]
    print(upload(path))
    for name, value in options:
        if name in ("-h", "--help"):
            help()
        if name in ("-i", "--ip"):
            pass
        if name in ("-o", "--out"):
            print('port is----', value)
    options, args = getopt.getopt(sys.argv[1:], "hp:i:", ["help", "ip=", "port="])

