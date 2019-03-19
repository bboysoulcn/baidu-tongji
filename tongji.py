# author: bboysoul
# email: bboysoulcn@gmail.com
# site: www.bboysoul.com
import requests
import json
import datetime

# 请修改下面这些变量
username = {你的百度统计用户名, 字符型}
password = {你的百度统计密码, 字符型}
token = {你的百度统计token点击管理->数据导出服务开通, 字符型}
site_id = {站点id点击站点详情的时候看url https://tongji.baidu.com/web/20885304/overview/index?siteId=??????问好就是你的站点id, 数字}
dingding_base_url = {钉钉机器人webhook的链接}
atMobiles = {钉钉群中你要@的人}


def get_pv_uv():
    baidu_base_url = "https://api.baidu.com/json/tongji/v1/ReportService/getData"
    today = str(datetime.date.today()).replace("-", "")
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1)).replace("-", "")
    body = {
        "header": {
            "username": username,
            "password": password,
            "token": token,
            "account_type": 1,
        },
        "body": {
            "site_id": site_id,
            "method": "overview/getTimeTrendRpt",
            "start_date": yesterday,
            "end_date": today,
            "metrics": "pv_count,visitor_count",
        }
    }
    req = requests.post(baidu_base_url, json.dumps(body))
    pv = json.loads(req.text)["body"]["data"][0]["result"]["items"][1][0][0]
    uv = json.loads(req.text)["body"]["data"][0]["result"]["items"][1][0][1]
    # 写入文件
    f1 = open("pvuv.txt", 'a')
    file_content = "pv: " + str(pv) + " uv: " + str(uv) + "\n"
    f1.write(file_content)
    f1.close()
    return pv, uv


def send_dingding():
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    msg = get_pv_uv()
    body = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "atMobiles": [
            atMobiles
            ],
            "isAtAll": "true"
        }
    }
    requests.post(dingding_base_url, json.dumps(body), headers=headers)

send_dingding()
print("job success")







