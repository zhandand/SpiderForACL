# SpiderForACL
spider for https://www.aclweb.org/anthology/ 爬取此网站论文的爬虫

## 统计信息
paper 61462  
pdf 59789  
video 1283  

## 依赖的第三方库
requests==2.23.0  
pymongo==3.11.2  
psutil==5.8.0  
tqdm==4.56.0  
beautifulsoup4==4.9.3  

## 运行代码
```python
python run.py
```

## 代码结构
.  
├── README.md  
├── requirements.txt  
├── run.py  
├── statistics.txt  
└── utils  
&nbsp;&nbsp;&nbsp;&nbsp;├── ACLScrawler.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── ACLUrlsCrawler.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── ClashControl.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── config.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── ContentDownloader.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── LevelUrls.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── PDFDownloader.py  
&nbsp;&nbsp;&nbsp;&nbsp;└── VideoDownloader.py  

## 代码逻辑
ACLScrawler为顶层类，拥有ACLUrlsCrawler，ContentDownloader，PDFDownloader，VideoDownloader四个类的成员，分别爬取https://www.aclweb.org/anthology/ 中的url，url对应的具体论文内容，pdf和视频。
### ACLUrlsCrawler
  遍历网站https://www.aclweb.org/anthology/ 获取会议的url, 遍历会议的 url 例如，https://www.aclweb.org/anthology/venues/aacl/ ，遍历某一年会议的urlhttps://www.aclweb.org/anthology/events/aacl-2020/ ，最后将所有的待爬取的url存到表中，每一个url有一个visit标记
### ContentDownloader
  遍历表中visit字段为false的url，爬取论文的基本内容并保存到表中，对于pdf和video字段不为空的数据，将待爬取的pdf和video的url保存到各自的表中，同样有一个visit标记。论文爬取完成后更新其url的visit字段
### PDFDownloader
  遍历表中visit字段为false的url，爬取pdf并更新url的visit字段，同时在基本信息表中更新pdf的文件路径
### VideoDownloader
  遍历表中visit字段为false的url，向视频网站发起请求并解析获取视频，爬取视频并更新url的visit字段，同时在基本信息表中更新pdf的文件路径。由于视频网站被墙了以及采取了反爬虫的测录额，采用了ip池和ip代理的技术


