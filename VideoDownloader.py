import os
import requests
import pymongo

class VideoManager():
    '''
    爬取论文视频
    '''
    def __init__(self):
        # self.siteUrls = siteUrls
        self.database = "ACLAnthology"
        self.collection = "Video"
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")

    def getVideoUrlsfromDB(self):
        '''
        从数据库中获取需要爬取视频的url
        :return:
        '''
        db = self.client[self.database]
        col = db[self.collection]
        return [url['url'] for url in col.find({"visit": False})]

    def addUrl(self,url):
        '''
            加入待爬取的视频的url
        :param url:
        :return:
        '''
        if(url ==""):
            return
        db = self.client[self.database]
        col = db[self.collection]
        if col.find_one({"url": url}) == None:
            col.insert_one({"url": url, "visit": False})
        return

    def getVideoUrlFromVimeo(self,siteUrl):
        '''
        :param siteUrl:https://vimeo.com/ 网站中的视频链接 例如 https://vimeo.com/383950369
        :return: 对应视频资源的url和视频格式
        '''
        headers = {
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        r = requests.get(siteUrl, headers=headers)
        videoUrls = []
        for file in r.content['files']:
            type = file['extension']
            download_url = file["download_url"]
            height = file["height"]
            videoUrls.append((download_url, type, height))

        #将url按照分辨率排序
        sorted(videoUrls, key=lambda video: video[2])
        if(videoUrls):
            # 下载分辨率最低的文件
            return videoUrls[0][0], videoUrls[0][1]
        else:
            return None, None

    def getVideoUrlFromslideslive(self,siteUrl):
        '''
        :param siteUrl:https://slideslive.com/ 网站中的视频链接 例如 https://slideslive.com/38928775/guiding-variational-response-generator-to-exploit-persona
        :return: 对应视频资源的url和视频格式
        '''
        pass

    def getVideoUrl(self,siteUrl):
        if("slideslive" in siteUrl):
            videoUrl, suffix = self.getVideoUrlFromslideslive(siteUrl)
        elif("vimeo" in siteUrl):
            videoUrl, suffix = self.getVideoUrlFromVimeo(siteUrl)

    def run(self):
        # todo:爬取论文逻辑
        pass
