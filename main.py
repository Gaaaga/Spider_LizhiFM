import requests
import re
import urllib.request
import requests
from bs4 import BeautifulSoup


# _ud.mp3:超高清; _hd.mp3:高清; _sd.m4a:低清

def get_music_lizhifm(url):
    id = url.rsplit('/', 1)[1]
    url = 'http://www.lizhi.fm/media/url/{}'.format(id)
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    html = requests.get(url, headers=headers).json()
    # print(html)
    if html['data']:
      mp3_url = html['data']['url']
      return mp3_url
    else:
      print("!!!"+html['msg'])
      return None
    

def downloadFromPage(startUrl):
  page = requests.get(startUrl)
  userId = re.findall('(/[0-9]{7}/)',startUrl)[0]
  downloadurl = get_music_lizhifm(startUrl)
  urlList = []
  bs = BeautifulSoup(page.content, features='lxml')
  if downloadurl:
    title = bs.select(".audioName")[0].text
    print(title)
    urllib.request.urlretrieve(downloadurl, './download/'+title+'.mp3')
  # get next url
  for link in bs.findAll('a'):
      url = link.get('href')
      downloadableUrl = re.findall('(^[0-9]{19}$)', url)
      if downloadableUrl:
        urlList.append(downloadableUrl[0])
  if(len(urlList) == 2):
    nextUrl = 'https://www.lizhi.fm'+userId+urlList[1]
    print('nextUrl: ' + nextUrl)
    downloadFromPage(nextUrl)
  else:
    print('urlList length error:'+ urlList)
    exit()


if __name__ == '__main__':
    print('*' * 30 + 'ready to download' + '*' * 30)
    url = input('[请输入初始下载链接]:')
    downloadFromPage(url)
