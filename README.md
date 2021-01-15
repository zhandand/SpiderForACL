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

## 工作流程
1. 从网站https://www.aclweb.org/anthology/ 获取到所有会议的url，再获取对应会议所有年份的url，最后获取所有论文的url并保存在数据库中。、
2. 对于第1步中获取到的论文url, 发送request的get请求获取论文的标题，作者，摘要，发布组织，年份，pdf的url，代码的url，视频url等相关信息，保存至mongodb中，并将pdf和视频的url保存至对应表中
3. 为了实现增量式爬取，我们将论文的url，pdf的url和视频的url保存置mongodb中，并且每条url数据对应一个visit字段以指示是否爬取了此条url对应的数据
4. 根据表中visit字段为false的url分别爬取pdf和视频数据。其中由于视频网站被墙以及反爬虫的策略，我们采用了IP代理和IP的技术

### 程序入口
  调用ACLScrawler的run函数  
  1. 调用ACLUrlsCrawler的run函数爬取所有论文的url(按照会议-某年会议的顺序遍历)
  2. 调用ContentDownloader的run函数爬取数据表中所有visit字段为false的url对应的基本论文信息
  3. 调用PDFDownloader的run函数爬取爬取数据表中所有visit字段为false的url对应的pdf
  4. 调用VideoDownloader的run函数爬取爬取数据表中所有visit字段为false的url对应的视频

