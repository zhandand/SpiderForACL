import requests
import pymongo
import LevelUrls.LevelUrls as lu

class PDFManager():
    '''
    爬取论文pdf
    '''
    def __init__(self):
        self.database = "ACLAnthology"
        self.collection = "PDF"
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.pdfUrls = self.getPDFUrlsfromDB()

    def getPDFUrlsfromDB(self):
        db = self.client[self.database]
        col = db[self.collection]
        return [url['url'] for url in col.find({"visit": False})]

    def get_content(self, url):
        try:
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
            response = requests.get(url, headers={'User-Agent': user_agent})
            response.raise_for_status()  # 如果返回的状态码不是200， 则抛出异常;
            response.encoding = response.apparent_encoding  # 判断网页的编码格式， 便于respons.text知道如何解码;
        except Exception as e:
            print("爬取错误")
        else:
            return response.content

    def downloadFile(self,url, fileName):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
        r = requests.get(url, headers={'User-Agent': user_agent}, stream=True)
        with open(fileName, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return

    def updateUrl(self,url):
        '''
            已经爬过的pdf更新数据库的visit标记
        :param url:
        :return:
        '''
        db = self.client[self.database]
        col = db[self.collection]
        col.update_one({"url": url}, {"$set": {"visit": True}})

    def addUrl(self,url):
        '''
            加入待爬取的pdf的url
        :param url:
        :return:
        '''
        if(url == ""):
            return
        db = self.client[self.database]
        col = db[self.collection]
        if col.find_one({"url":url})==None:
            col.insert_one({"url":url,"visit":False})
        return

    def run(self):
        for pdfurl in self.pdfUrls:
            try:
                pdfurlSplit = pdfurl.split("/")
                fileName = pdfurlSplit[len(pdfurlSplit)-1]
                self.downloadFile(pdfurl,fileName)
            except Exception as e:
                lu.ErrorUrlManeger(pdfurl,e)
        print("PDF downloading done")