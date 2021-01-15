# SpiderForACL
spider for https://www.aclweb.org/anthology/  
支持增量式爬取    
使用了代理和ip池

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
&nbsp;&nbsp;&nbsp;&nbsp;├── LevelUrls.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── PDFDownloader.py  
&nbsp;&nbsp;&nbsp;&nbsp;└── VideoDownloader.py  

## 代码逻辑
ACLScrawler为顶层类，拥有ACLUrlsCrawler，ContentDownloader，PDFDownloader，VideoDownloader四个类的成员，分别用来爬取https://www.aclweb.org/anthology/ 中的url，url对应的具体论文内容，pdf和视频。
### 程序入口
  调用ACLScrawler的run函数  
  1. 调用ACLUrlsCrawler的run函数爬取https://www.aclweb.org/anthology/venues/aacl/ 中的所有论文的url(按照会议-某年会议的顺序遍历)
  2. 调用ContentDownloader的run函数爬取数据表中所有visit字段为false的url对应的基本论文信息
  3. 调用PDFDownloader的run函数爬取爬取数据表中所有visit字段为false的url对应的pdf
  4. 调用VideoDownloader的run函数爬取爬取数据表中所有visit字段为false的url对应的视频

