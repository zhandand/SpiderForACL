import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
           "Referer": "https: //9xbuddy.org/sites/zh/slideslive"
           }

# r = requests.get("https://vimeo.com/383950369?action=load_download_config",headers=headers)
r = requests.get("https://9xbuddy.org/process?url=https://slideslive.com/38926829", headers=headers)


print(r.content)

with open("video.html","wb") as f:
    f.write(r.content)
