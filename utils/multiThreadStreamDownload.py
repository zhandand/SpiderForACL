import threading

import requests
import threadpool
# from multiprocessing.pool import ThreadPool
from clint.textui import progress

num = 0
lock = threading.Lock()


def getVideoUrl(siteUrl):
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
        videoUrls.append((download_url,type,height))

    # 将url按照分辨率排序
    sorted(videoUrls, key= lambda video:video[2])
    if(videoUrls):
        # 下载分辨率最低的文件
        return videoUrls[0][0],videoUrls[0][1]
    else:
        return None,None

def getThenSave(url,fileName,suffix):
    global num
    print("downloading...")
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
    }
    r = requests.get(url, headers=headers,stream = True)
    print(r.content)
    total_length = int(r.headers.get('content-length'))

    lock.acquire()
    try:
        pdfID = num
        num +=1
    finally:
        lock.release()
    with open(fileName+"."+suffix,"wb") as f:
        for chunk in progress.bar(r.iter_content(chunk_size=1024),expected_size=(total_length)/1024+1,width=100):
            if  chunk:
                f.write(chunk)
    return

def download(urls,threadNum = 5):
    pool = threadpool.ThreadPool(threadNum)
    request_list = threadpool.makeRequests(downLoadVideo,urls)
    [pool.putRequest(req) for req in request_list]
    pool.wait()

def prepareUrls():
    urls = []
    # for i in range(4000,4009):
    #     urls.append("https://www.aclweb.org/anthology/P19-" + str(i)+".pdf")
    # urls.append(parse.quote("https://player.vimeo.com/play/1613661222?s=383950369_1608733604_a96486b39380a37d4845613b27b1307b&loc=external&context=Vimeo%5CController%5CClipController.main&download=1"))
    # urls.append("https://player.vimeo.com/play/1613661826?s=383950369_1608734369_55f7e6381a646232da1bf3049002fcd1&loc=external&context=Vimeo%5CController%5CClipController.main&download=1")
    urls.append("https://vimeo.com/383950369?action=load_download_config")
    return urls

def downLoadVideo(url):
    videoUrl,suffix = getVideoUrl(url)
    # getThenSave(videoUrl,,suffix)





if __name__ == '__main__':
    download(prepareUrls())
    # url_response("https://www.aclweb.org/anthology/P19-4000.pdf")