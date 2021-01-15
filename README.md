# SpiderForACL
spider for https://www.aclweb.org/anthology/ 爬取此网站论文的爬虫

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
├── url.text  
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
