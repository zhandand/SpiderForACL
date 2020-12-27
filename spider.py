import requests
from bs4 import BeautifulSoup
import urllib.parse
import bs4
import pymongo

def downloadFile(fileUrl,destination):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
    r = requests.get(fileUrl, headers={'User-Agent': user_agent},stream=True)
    with open(destination,"wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return

def get_content(url):
    try:
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
        response = requests.get(url,  headers={'User-Agent': user_agent})
        response.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
        response.encoding = response.apparent_encoding  # 判断网页的编码格式， 便于respons.text知道如何解码;
    except Exception as e:
        print("爬取错误")
    else:
        print(response.url)
        print("爬取成功!")
        return  response.content

def parse(content,num):
    soup = BeautifulSoup(content,'lxml')
    title = soup.title.string
    print(title)
    citation_author_raw = soup.find_all('meta')
    citation_authors = []
    for citation_author in citation_author_raw:
        try:
            if(citation_author.attrs['name'] == "citation_author"):
                citation_authors.append(citation_author.attrs['content'])
        except Exception as e:
            pass

    try:
        # 去掉字符串"abstract"
        abstract_tag = soup.find("div", class_="acl-abstract")
        abstract_raw = abstract_tag.text[8:]
        abstract_words_raw = abstract_raw.split(' ')
        abstract_words = []
        for word in abstract_words_raw:
            if word != '':
                if (word.endswith("\n")):
                    abstract_words.append(word[:-1])
                else:
                    abstract_words.append(word)
        abstract = " ".join(abstract_words)
    except Exception as e:
        abstract = ""

    detail_tags = soup.find("div" , class_ = "acl-paper-details" ).find("dl")
    key_tags = detail_tags.find_all("dt")
    value_tags = detail_tags.find_all("dd")
    details = {}
    for key,value in zip(key_tags,value_tags):
        if(key.text[:-1] == "Dataset"):
            url = value.find("a")['href']
            details[key.text[:-1]] = url
            # downloadFile(url,"./PDFs/"+str(num)+".pdf")
        elif(key.text[:-1] == "Video"):
            url = value.find("a")['href']
            details[key.text[:-1]] = url
        else:
            details[key.text[:-1]] = value.text

    if("publicationOrg" not in details.keys()):
        details["publicationOrg"] = ""
    if ("Year" not in details.keys()):
        details["Year"] = ""
    if ("PDF" not in details.keys()):
        details["PDF"] = ""
    if ("URL" not in details.keys()):
        details["URL"] = ""
    if ("Dataset" not in details.keys()):
        details["Dataset"] = ""
    if ("Video" not in details.keys()):
        details["Video"] = ""

    return {
        "title" : title,
        "authors" : ", ".join(citation_authors),
        "abstract":abstract,
        "publicationOrg":details['Publisher'],
        "year":details['Year'],
        "pdfUrl":details['PDF'],
        "pdfPath":"",
        "publicationUrl":details['URL'],
        "codeUrl":"",
        "datasetUrl":details['Dataset'],
        "videoUrl":details['Video'],
        "videoPath":""
    }

def savePaperInfo(paperInfo,database ="ACLAnthology",collection = "ACLAnthology"):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[database]
    col = db[collection]
    #检查标题重复
    if(col.find_one({ "title": paperInfo["title"]}) != None):
        return

    col.insert_one(paperInfo)

def prepareUrls():
    urls = []
    for i in range(4000,4009):
        urls.append("https://www.aclweb.org/anthology/P19-" + str(i))
    return urls

if __name__ == '__main__':
    # for url in prepareUrls():
    #     content = get_content(url)
    #     paperInfo =  parse(content,0)
    #     savePaperInfo(paperInfo)
    # getUrlsfromSecondLevel("https://www.aclweb.org/anthology/venues/anlp/")
    # getUrlsfromTopLevel(baseUrl+"/anthology/")
    pass


