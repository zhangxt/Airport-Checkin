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
    session.get(base_url, verify=False)
    login_url = base_url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    response = session.post(login_url, post_data, headers=headers, verify=False)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': base_url + '/user'
    }
    response = session.post(base_url + '/user/checkin', headers=headers,
                            verify=False)
    response = json.loads(response.text)
    print(response)
    print(response['msg'])
    return response['msg']



def send_wechat_msg(content, webhook_url):
    data = {"msgtype": "markdown", "markdown": {"content": content}}
    r = requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), verify=False)
    return r.text, r.status_code

def sync_send_wechat_msg(content):
    t = threading.Thread(target=send_wechat_msg, args=(content,qiwei))
    t.start()


curtime = str(datetime.now())
result = checkin(email=os.environ.get('EMAIL1'))
sync_send_wechat_msg(os.environ.get('EMAIL1')+"---"+curtime+result)

result = checkin(email=os.environ.get('EMAIL2'))
sync_send_wechat_msg(os.environ.get('EMAIL2')+"---"+curtime+result)


result = checkin(email=os.environ.get('EMAIL3'))
sync_send_wechat_msg(os.environ.get('EMAIL3')+"---"+curtime+result)

result = checkin(email=os.environ.get('EMAIL4'))
sync_send_wechat_msg(os.environ.get('EMAIL4')+"---"+curtime+result)
