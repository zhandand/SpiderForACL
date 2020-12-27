import pymongo

class SecondLevelManager:
    def __init__(self):
        '''
                 https://www.aclweb.org/anthology/venues/anlp/ 为2级
        '''
        self.database = "ACLAnthology"  # 爬取的url将要保存的数据库名

        self.collection = "SecondLevelUrls"  # 爬取的url将要保存的表名
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")

    def getSecondLevelUrls(self):
        '''
        检查数据库中未被访问的二级url
        :return:
        '''
        db = self.client[self.database]
        col = db[self.collection]
        urls = [url for url in col.find()]
        if(len(urls) == 0):
            return None
        else:
            UnvisitiUrls = col.find({"visit": False}, {"url": 1})
            return [url['url'] for url in UnvisitiUrls]

    def saveSecondLevelUrls(self,urls):
        '''
        保存二级url
        :param urls:
        :return:
        '''
        db = self.client[self.database]
        col = db[self.collection]
        Urls = []
        for url in urls:
            Urls.append({"url":url,"visit":False})
        if len(Urls)==0:
            return
        else:
            col.insert_many(Urls)

    def updateSecondLevelUrls(self,url):
        '''
        标记已经访问过的url
        :param url:
        :return:
        '''
        db = self.client[self.database]
        col = db[self.collection]
        col.update({"url": url}, { "$set": { "visit": True } })

class ErrorUrlManeger:
    '''
    处理出错的url,保存到errorUrl表中
    '''
    def __init__(self,url,error):
        self.database = "ACLAnthology"  # 爬取的url将要保存的数据库名
        self.collection = "errorUrl"  # 爬取的url将要保存的表名
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = self.client[self.database]
        col = db[self.collection]
        col.insert_one({"url":url,"error":error})