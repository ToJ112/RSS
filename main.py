'''
Author: Leo Lee (leejianzhao@gmail.com)
Date: 2021-07-18 16:34:45
LastEditTime: 2022-03-24 08:32:11
FilePath: \RSS\main.py
Description:
'''

import base64
import requests
import json
import time
import re
import base64
# import logging
# import traceback
import os
import random
import datetime
import feedparser
import urllib
import yaml
# import utils
# import wxpusher
# import pytz
import string

# from lxml.html import fromstring
import urllib.parse
import urllib3
urllib3.disable_warnings()

dirs = './subscribe'

def log(msg):
    time = datetime.datetime.now()
    print('['+time.strftime('%Y.%m.%d-%H:%M:%S')+']:'+msg)


# def getFeeds():
#     rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
#     current = rss["entries"][0]
#     result = re.findall(r"vmess://(.+?)</div>", rss["entries"][0]["summary"])
#     i = 0
#     dy = ''
#     for point in result:
#         i = i + 1
#         dy += 'vmess://'+point+'\n'
#         logging.info('【'+('%02d' % i) + '】 vmess://' + point)
#     return base64.b64encode(dy.encode('utf-8'))

# 获取文章地址


def getSubscribeUrl():
    try:
        rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
        current = rss["entries"][0]
        v2rayList = re.findall(
            r"v2ray\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        clashList = re.findall(
            r"clash\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        if v2rayList:
            v2rayTxt = requests.request(
                "GET", v2rayList[len(v2rayList)-1].replace('amp;',''), verify=False)
            with open(dirs + '/v2ray.txt', 'w') as f:
                f.write(v2rayTxt.text)
            # print(v2rayTxt.text)
        if clashList:
            clashTxt = requests.request(
                "GET", clashList[len(clashList)-1].replace('amp;',''), verify=False)
            day = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            with open(dirs + '/clash.yml', 'w',encoding='utf-8') as f:
                f.write(clashTxt.text.replace('mattkaydiary.com',day))
            # print(clashTxt.text)
    except Exception as e:
        log('RSS load error: '+e.__str__())

def get_mattkaydiary():
    log('begin get_mattkaydiary')
    v2ray_add=None
    try:
        rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
        current = rss["entries"][0]
        v2rayList = re.findall(r"v2ray\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        clashList = re.findall(r"clash\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        if v2rayList:
            v2ray_add=v2rayList[len(v2rayList)-1].replace('amp;', '').strip()
            v2rayTxt = requests.request(
                "GET", v2ray_add)
            with open(dirs + '/v2ray_mat.txt', 'w') as f:
                f.write(v2rayTxt.text)
            # print(v2rayTxt.text)
        if clashList:
            clashTxt = requests.request(
                "GET", clashList[len(clashList)-1].replace('amp;','').strip(), verify=False)
            day = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            with open(dirs + '/clash_mat.yml', 'w',encoding='utf-8') as f:
                f.write(clashTxt.text.replace('mattkaydiary.com',day))
    except Exception as e:
        log('can not get_mattkaydiary:'+e.__str__())
    return v2ray_add

# def IP2name(ip):
#     try:
#         res=requests.get(f'http://ip-api.com/json/{ip}?fields=country,countryCode,city&lang=zh-CN', timeout=10).json()
#         return f"{ip}@{res['country']}({res['countryCode']})-{res['city']}/"+''.join(random.sample(string.ascii_letters + string.digits, 3))
#     except Exception as e:
#         log('IP2name: '+ip+': '+e.__str__())
#         return ip+''.join(random.sample(string.ascii_letters + string.digits, 8))

def IP2name(ip):
    return ip+''.join(random.sample(string.ascii_letters + string.digits, 8))


# https://github.com/p4gefau1t/trojan-go/issues/132
# trojan-go://
#     $(trojan-password)
#     @
#     trojan-host
#     :
#     port
# ?
#     sni=$(update.microsoft.com)&
#     type=$(original|ws|h2|h2+ws)&
#         host=$(update-01.microsoft.com)&
#         path=$(/update/whatever)&
#     encryption=$(ss;aes-256-gcm:ss-password)&
#     plugin=$(...)
# #$(descriptive-text)
# 特别说明：$() 代表此处需要 encodeURIComponent。
# example:
#   trojan://f@uck.me/?sni=microsoft.com&type=ws&path=%2Fgo&encryption=ss%3Baes-256-gcm%3Afuckgfw


def protocol_decode(proxy_str):
    proxy={}
    # url = urllib.parse.urlparse(proxy_str)
    proxy_str_split=proxy_str.split('://')
    if proxy_str_split[0] == 'trojan':
        pass
        # try:
        #     tmp=urllib.parse.urlparse(proxy_str)
        #     server=tmp.hostname
        #     port=tmp.port
        #     password=tmp.username
        #     # password, addr_port = proxy_str_split[1].split('@')
        #     # password = urllib.parse.unquote(password)
        #     # addr, port = addr_port.rsplit(':', 1)
        #     # if addr[0] == '[':
        #     #     addr = addr[1:-1]
        #     # port = int(port)
        #     proxy={
        #         # "name"      :   ''.join(random.sample(string.ascii_letters + string.digits, 8)), #urllib.parse.unquote(url.fragment),
        #         "name"      :   IP2name(server),
        #         "type"      :   "trojan",
        #         "server"    :   server,
        #         "password"  :   password,
        #         "port"      :   port,
        #         # "sni"       :   server
        #     }
        # except Exception as e:
        #     log('Invalid trojan URL:'+proxy_str)
        #     log(e.__str__())
    elif proxy_str_split[0] == 'vmess':
        try:
            tmp=json.loads(base64.b64decode(proxy_str_split[1]+'=='))
            if tmp["add"]!='127.0.0.1':
                proxy={
                    # "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)),#tmp["ps"],
                    "name"      :   IP2name(tmp.get("add")),
                    "type": "vmess",
                    "server": tmp.get("add"),
                    "port": tmp.get("port"),
                    "uuid": tmp.get("id"),
                    "alterId": tmp.get("aid"),
                    "cipher": "auto",
                    "network": tmp.get("net"),
                    'ucp':True,
                    'ws-path':tmp.get('path'),
                    'ws-headers':{'Host':tmp['host']} if tmp.__contains__('host') else None,
                    "tls": True if tmp.get("tls") == "tls" or tmp.get("net") == "h2"else False,
                }
        except Exception as e:
            log('Invalid vmess URL:'+proxy_str)
            log(e.__str__())
    elif proxy_str_split[0] == 'ss':
        tmp=urllib.parse.urlparse(proxy_str)
        if tmp.username is not None:
            server=tmp.hostname
            port=tmp.port
            cipher,password=base64.b64decode(tmp.username+'==').decode().split(':')
        else:
            tmp=base64.b64decode(tmp.netloc+'==').decode()
            cipher,other,port=tmp.split(':')
            password,server=other.split('@')
        if cipher and password and server and port:
            proxy={
                # "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)), #urllib.parse.unquote(url.fragment),
                "name"      :   IP2name(server),
                "type": "ss",
                "server": server,
                "port": port,
                "password": password,
                "alterId": 2,
                "cipher": cipher,
            }
    elif proxy_str_split[0] == 'ssr':
        #todo
        #   - name: "ssr"
        #     type: ssr
        #     server: server
        #     port: 443
        #     cipher: chacha20-ietf
        #     password: "password"
        #     obfs: tls1.2_ticket_auth
        #     protocol: auth_sha1_v4
        proxy={}
    return proxy

def load_subscribe_url(url):
    if not url: return []
    log('begin load_subscribe_url: '+url)
    try:
        v2rayTxt = requests.request("GET", url, verify=False)
        return base64.b64decode(v2rayTxt.text+'==').decode('utf-8').splitlines()
    except Exception as e:
        log('load_subscribe_url: '+url+': '+e.__str__())
        return []


def load_subscribe(file):
    with open(file, 'rb') as f:
        raw=base64.b64decode(f.read()).decode('utf-8').splitlines()
    return raw

# def gen_clash_subscribe(proxies):
#     with open(r"./template/clash_proxy_group.yaml", 'r', encoding='UTF-8') as f:
#         proxy_groups = yaml.safe_load(f)
#     # print(proxy_groups)
#     for p in proxy_groups:
#         if not p.__contains__('proxies'):
#             p['proxies']=[n["name"] for n in proxies if n]
#     with open(r"./template/clash_tmp.yaml", 'r',encoding="utf-8") as f:
#         template = yaml.safe_load(f)
#     template["proxies"]=proxies
#     template["proxy-groups"]=proxy_groups
#     with open(r"./subscribe/tmp.yaml",'w', encoding="utf-8") as f:
#         yaml.dump(template,f, sort_keys=False,encoding="utf-8",allow_unicode=True)

def gen_clash_subscribe(proxies):
    with open(r"./subscribe/config.yml", 'r', encoding='UTF-8') as f:
        config = yaml.safe_load(f)
    config['proxies']=proxies
    proxies_name=[proxies[i]['name'] for i in range(len(proxies))]
    config['proxy-groups'][0]['proxies'].extend(proxies_name)
    config['proxy-groups'][1]['proxies']=proxies_name
    with open(r"./subscribe/clash.yml",'w', encoding="utf-8") as f:
        yaml.dump(config,f, sort_keys=False,encoding="utf-8",allow_unicode=True)

def gen_v2ray_subscribe(proxies):
    with open(dirs + '/v2ray.txt','wb') as f:
        f.write(base64.b64encode('\n'.join(proxies).encode('ascii')))

# 主函数入口
if __name__ == '__main__':
    log("RSS begin...")
    proxies=[]
    # getSubscribeUrl()
    # proxies.extend(load_subscribe(dirs + '/v2ray.txt'))
    proxies.extend(load_subscribe_url(get_mattkaydiary()))
    # gen_clash_subscribe(list(filter(None,map(protocol_decode,proxies))))
    proxies.extend(load_subscribe_url('https://jiang.netlify.app'))
    proxies.extend(load_subscribe_url('https://iwxf.netlify.app'))
    proxies.extend(load_subscribe_url('https://youlianboshi.netlify.com'))
    # proxies.extend(load_subscribe_url('https://fforever.github.io/v2rayfree'))
    # proxies.extend(load_subscribe_url('https://muma16fx.netlify.app'))
    # proxies.extend(load_subscribe_url('https://cdn.jsdelivr.net/gh/fggfffgbg/https-aishangyou.tube-@master/README.md'))
    # proxies.extend(load_subscribe_url('https://freev2ray.netlify.app/'))
    # proxies.extend(load_subscribe_url('https://raw.githubusercontent.com/eycorsican/rule-sets/master/kitsunebi_sub'))
    proxies.extend(load_subscribe_url('https://sspool.herokuapp.com/vmess/sub'))
    proxies.extend(load_subscribe_url('https://raw.githubusercontent.com/freefq/free/master/v2'))
    # proxies.extend(load_subscribe_url(''))
    gen_clash_subscribe(list(filter(None,map(protocol_decode,proxies))))
    gen_v2ray_subscribe(proxies)
