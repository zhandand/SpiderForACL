# coding : utf - 8
import requests
import psutil


class ClashControl:
    clash_host = "127.0.0.1"
    controller_port = "65117"

    def __init__(self):
        process_list = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
            except psutil.NoSuchProcess:
                pass
            else:
                if "clash" in pinfo['name']:
                    print("CLash process detected, pid : " + str(pinfo['pid']))
                    print("Clash host : " + self.clash_host + ", controller_port : " + self.controller_port)
                    return
        print("Clash not found. Exit.")
        exit(-1)

    def getProxies(self):
        api = "http://" + self.clash_host + ":" + self.controller_port + "/proxies"
        # api = "http://damneasy.top:5555/random"
        r = requests.get(api)
        raw_list = list(r.json()['proxies'])
        print(raw_list)
        i = 0
        proxyList = []
        for proxyName in raw_list:
            if (("IEPL" or "IPLC") in proxyName or "多协议" in proxyName or "香港" in proxyName) and ("游戏" not in proxyName):
                proxyList.append(proxyName)

        # for proxyName in proxyList:
        #     print(proxyName)
        return proxyList




if __name__ == '__main__':
    clashControl = ClashControl()
    clashControl.getProxies()
