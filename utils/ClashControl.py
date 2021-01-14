# coding : utf - 8
import json
import random

import requests
import psutil


class ClashControl:
    clash_host = "127.0.0.1"
    controller_port = "65117"
    proxy_port = "1717"
    proxyList = {}

    def __init__(self):
        # process_list = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
            except psutil.NoSuchProcess:
                pass
            else:
                if "clash" in pinfo['name']:
                    print("CLash process detected, pid : " + str(pinfo['pid']))
                    print("Clash host : " + self.clash_host + ", controller_port : " + self.controller_port)
                    self.proxyList = self.getProxies()
                    return
        print("Clash not found. Exit.")
        exit(-1)

    def getProxies(self):
        api = "http://" + self.clash_host + ":" + self.controller_port + "/proxies"
        r = requests.get(api)
        raw_list = list(r.json()['proxies'])
        # print(raw_list)
        proxyList = []
        for proxyName in raw_list:
            if (
                    "IEPL" in proxyName or "IPLC" in proxyName or "PVCC" in proxyName
                    or "多协议" in proxyName or "香港" in proxyName) \
                    and ("游戏" not in proxyName):
                proxyList.append(proxyName)

        # for proxyName in proxyList:
        #     print(proxyName)
        return proxyList

    def checkProxy(self, proxyName):
        # proxyName = "FakeProxy"
        if proxyName not in self.proxyList:
            print("Wrong proxy name")
            return
        header = {
            "Content-Type": "application/json"
        }
        payload = {
            "timeout": 3000,  # ms
            "url": "http://vimeo.com"
        }
        # proxyName = "FakeProxy"
        api = "http://" + self.clash_host + ":" + self.controller_port + "/proxies/" + proxyName + "/delay"
        # print(api)
        r = requests.get(api, headers=header, params=payload)
        # print(r.json())
        if list(r.json()).count("delay"):
            print("proxy " + proxyName + " available, delay:" + str(r.json()["delay"]))
            return True
        else:
            print("proxy unavailable. Error message: " + r.json()["message"])
            return False

    def getRandomProxy(self):
        randomProxy = self.proxyList[random.randint(0, len(clashControl.proxyList) - 1)]
        print("Get a random proxy from the proxy list: " + randomProxy)
        return randomProxy

    def changeProxyByProxynamne(self, proxyName):
        if proxyName not in self.proxyList:
            print("Wrong proxy name.")
            return
        header = {
            "Content-Type": "application/json",
        }
        payload = "{\"name\":\"" + str(proxyName) + "\"}"
        api = "http://" + self.clash_host + ":" + self.controller_port + "/proxies/国外流量"
        # print(api,payload,sep=', ')
        r = requests.put(api, headers=header, data=payload.encode('utf-8'))
        if r.status_code == 204:
            ip_info = dict(requests.get("http://ip.gs/json").json())
            print("Change proxy to " + proxyName + " successfully, ip: " + ip_info["ip"] + ", location: " + ip_info[
                "city"] + "," + ip_info["country"])
            return True
        else:
            print("Error:", r.status_code, r.text)
            return False


if __name__ == '__main__':
    clashControl = ClashControl()
    # clashControl.getProxies()
    randomProxy = clashControl.getRandomProxy()
    if clashControl.checkProxy(randomProxy):
        clashControl.changeProxyByProxynamne(randomProxy)
