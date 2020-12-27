from tqdm import tqdm

import utils.LevelUrls as lu
from ACLUrlsCrawler import ACLUrlsCrawler
from ContentDownloader import ContentManager
from PDFDownloader import PDFManager
from VideoDownloader import VideoManager


class ACLScrawler:
    def __init__(self):
        self.urlScrawler = ACLUrlsCrawler()
        self.pdfManager = PDFManager()
        self.videoManager = VideoManager()
        self.contenManager = ContentManager()

    def run(self):
        # 爬取论文的基本信息
        urls = self.urlScrawler.getACLUrls()
        pbar = tqdm(urls)
        for url in pbar:
            try:
                pbar.set_description("Crawling %s" % url)
                # 爬取并保存论文基本内容
                paperInfo = self.contenManager.run(url)
                # 加入待爬取的pdf url
                self.pdfManager.addUrl(paperInfo['pdfUrl'])
                # 加入待爬取的视频 url
                self.videoManager.addUrl(paperInfo['videoUrl'])
                # 爬取数据后更新url visit字段
                self.urlScrawler.updateUrl(url)
            except Exception as e:
                lu.ErrorUrlManeger(url, e)

        # todo
        # # 爬取论文的pdf
        # self.pdfManager.run()
        # # 爬取论文的视频
        # self.videoManager.run()

# if __name__ == '__main__':
#     aclscrawler = ACLScrawler()
# aclscrawler.updateUrl("")
