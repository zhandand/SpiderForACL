import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}

# r = requests.get("https://vimeo.com/383950369?action=load_download_config",headers=headers)
r = requests.get("https://slideslive.com/38928775/guiding-variational-response-generator-to-exploit-persona",headers=headers)


print(r.content)

with open("video.html","wb") as f:
    f.write(r.content)
