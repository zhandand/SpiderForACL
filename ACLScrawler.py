from ACLUrlsCrawler import ACLUrlsCrawler
import requests
from bs4 import BeautifulSoup
import pymongo
import LevelUrls.LevelUrls as lu
from PDFDownloader import PDFManager
from VideoDownloader import VideoManager
from ContentDownloader import ContentManager

class ACLScrawler:
    def __init__(self):
        self.urlScrawler = ACLUrlsCrawler()
        self.pdfManager = PDFManager()
        self.videoManager = VideoManager()
        self.contenManager = ContentManager()
        self.database = "ACLAnthology"
        self.collection = "ACLAnthology"
        self.urlCollection = "Urls"
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")

    def run(self):
        # 爬取论文的基本信息
        urls = self.urlScrawler.getACLUrls()
        for url in urls:
            try:
                # 爬取并保存论文基本内容
                paperInfo =  self.contenManager.run(url)
                # 加入待爬取的pdf url
                self.pdfManager.addUrl(paperInfo['pdfUrl'])
                # 加入待爬取的视频 url
                self.videoManager.addUrl(paperInfo['videoUrl'])
                # todo:爬取数据后更新url visit字段
                # self.updateUrl(url)
            except Exception as e:
                lu.ErrorUrlManeger(url,e)

        # 爬取论文的pdf
        self.pdfManager.run()
        # 爬取论文的视频
        self.videoManager.run()


if __name__ == '__main__':
    aclscrawler = ACLScrawler()
    # aclscrawler.updateUrl("")
