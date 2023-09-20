import threading

import requests
import json
import os
from datetime import datetime

requests.packages.urllib3.disable_warnings()


qiwei = os.environ.get('qiwei')



def checkin(email=os.environ.get('EMAIL'), password=os.environ.get('PASSWORD'),
            base_url=os.environ.get('BASE_URL'), ):
    email = email.split('@')
    email = email[0] + '%40' + email[1]
    session = requests.session()
    ## 使用session对象发送一个GET请求到base_url，并且禁用了证书验证（verify=False）。这个请求的目的可能是为了建立与服务器的连接或者获取一些必要的信息。
    #session.get(base_url, verify=False)
    login_url = base_url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    
    response = session.post(login_url, post_data, headers=headers)
    ##, verify=False)
    ## 需要修改验证这部分 0827

    # Access the cookies from the session
    cookies = session.cookies

    # Iterate over the cookies and print their content
    for cookie in cookies:
       print(cookie.name, cookie.value)
                        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': base_url + '/user'
    }
    response = session.post(base_url + '/user/checkin', headers=headers)
    ## ,
    ## verify=False)


    print(response)  
    try:
        print(response.text)
        response = json.loads(response.text)
        print(response)
        print(response['msg'])
        return response['msg']
    except Exception as e:
        print("error")
        return "error"



def send_wechat_msg(content, webhook_url):
    data = {"msgtype": "markdown", "markdown": {"content": content}}
    r = requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), verify=False)
    print(data)
    return r.text, r.status_code

def sync_send_wechat_msg(content):
    t = threading.Thread(target=send_wechat_msg, args=(content,qiwei))
    t.start()


curtime = str(datetime.now())
result = checkin(email=os.environ.get('EMAIL1'))
sync_send_wechat_msg(os.environ.get('EMAIL1')+"--1-"+curtime+result)

result = checkin(email=os.environ.get('EMAIL2'))
sync_send_wechat_msg(os.environ.get('EMAIL2')+"--2-"+curtime+result)


result = checkin(email=os.environ.get('EMAIL3'))
sync_send_wechat_msg(os.environ.get('EMAIL3')+"--3-"+curtime+result)

result = checkin(email=os.environ.get('EMAIL4'))
sync_send_wechat_msg(os.environ.get('EMAIL4')+"--4-"+curtime+result)
