import urllib.request,urllib.error
import datetime
import re
import os.path
from selenium import webdriver
import threading
import time
import random
import requests
import sys
from bs4 import BeautifulSoup

dic_path = r"C:\Users\JM-OP21\web_crawler\crawler_5278\source"

class video5278(object):
    def __init__(self, content_url, page_list):
        self.content_url = content_url
        self.page_list = page_list

    def save_file(self,this_download_url,title):
        time1=datetime.datetime.now()
        video_name = title
        path = os.path.join(dic_path,video_name)
        if (os.path.isfile(path)):
            file_size=os.path.getsize(path)/1024/1024
            print ("File %s(%sMb)already exists " %(path,str(file_size)))
            return True
        else:
            f = urllib.request.urlopen(this_download_url)
            data = f.read()
            try:
                with open(path, "wb") as code:
                    code.write(data)
                code.close()
            except OSError:
                print("OSError occurs")
                pass
            time2=datetime.datetime.now()
            use_time=time2-time1                     
            print ("Time used: %s"%(str(use_time)[:-7]))
            file_size=os.path.getsize(path)/1024/1024
            print ("File size: %s MB, Speed: %sMB/s"%( str(file_size),str(file_size/(use_time.total_seconds()))[:4]))


    def get_page_content(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
        res = requests.get(url, headers=headers)
        content = BeautifulSoup(res.text, features="html5lib")
        return content 

    def download_video(self,url,pageUrl,num,download_thread):
        req = urllib.request.Request(url)
        content = urllib.request.urlopen(req).read()
        content = content.decode('utf-8')
 
        while len(content)<100:
            print("try again...")
            content = urllib.request.urlopen(req).read()
            content = content.decode('utf-8')

        title_content = self.get_page_content(pageUrl)
        titles_moza = title_content.find_all('div',{'class':'mozaique'})
        title_under = [title for title in titles_moza[0].find_all('div',{'class':'thumb-under'})]
        if num%21 == 0:
            file_path__ = "video_title_"+str(download_thread)+".txt"
            for title_ in title_under:
                title_p = title_.find('p',{'class':'title'})
                title_a = title_p.find('a').text
                with open(file_path__,"a",encoding='utf-8') as f:
                    f.write("%s\n" % title_a)
                f.close()
        

        lowUrlRe = r"setVideoUrlLow\(\'(.+?)\'\);"
        patternLowUrl = re.compile(lowUrlRe)
        to_find = content
        matchLowUrl = patternLowUrl.search(to_find)

        os_path = r"C:\Users\JM-OP21\web_crawler\crawler_5278\video_title_"+str(download_thread)+r".txt"
        if os.path.exists(os_path):
            video__ = "video_title_"+str(download_thread)+".txt"
            with open(video__,"r",encoding = 'utf-8') as f:
                line = f.readlines()
                title = line[num%21].strip()+".mp4"
            f.close()
        lowUrl = ""
        if matchLowUrl:
            lowUrl = matchLowUrl.group(1)
        if len(lowUrl)>0:
            print("正在下載該分頁第 ",num%21+1, " 部影片")
            if title.find("http") != -1:
                return True
            else:
                self.save_file(lowUrl,title)
        return True


    def getPageUrls(self,pages, start,end):
        for p in range(int(start),int(end)):
            page_url = "http://www.5278.cc/forum.php?mod=forumdisplay&fid=23&typeid=431&typeid=431&filter=typeid&page="+str(p)
            pages.add(page_url)
        return pages

    def getContentUrls(self,start_url,txt_thread):
        browser = webdriver.Chrome("C:/Users/JM-OP21/chromedriver.exe")
        browser.get(start_url)

        # 通過css selector 查找
        #urls = browser.find_elements_by_css_selector('.thumb a')
        urls = browser.find_elements_by_css_selector('.title a')
        
        i = 1
        for x in urls:
            url = x.get_attribute('href')
            if url not in self.content_url:
                i+=1
                self.content_url.add(url)
                if i == 28:
                    file_path = r"C:\Users\JM-OP21\web_crawler\crawler_5278\page_url_list_"+str(txt_thread)+r".txt"
                    with open(file_path,"a") as f:
                        for item in self.content_url:
                            f.write("%s\n" % item)
                    f.close()
                    self.content_url = set()
                    break
            else:
                print("Already downloaded")
        time.sleep(5)
        browser.quit()
        return True
    
    


if __name__ == "__main__":
    c, p, i = set(), set(), 0
    x = video5278(c,p)
    x.save_file("http://cp3.hboav.com/check/hbo7/hls/files/mp4/D/O/k/DOkK2.mp4/index.m3u8","test")
    # p1, p2 = sys.argv[1], sys.argv[2]
    # pageurl = x.getPageUrls(set(),p1,p2)
    # for page_url in sorted(list(pageurl)):
    #     print("Getting the content urls in page ",re.findall(r'\d+', page_url)[-1])
    #     x.getContentUrls(page_url,p1)
    # file_path_ = "page_url_list_"+str(p1)+".txt"
    # with open(file_path_,"r") as f:
    #     for item in f.readlines():
    #         p = "http://www.5278.cc/forum.php?mod=forumdisplay&fid=23&typeid=431&typeid=431&filter=typeid&page="+str(i//21)
    #         i+=1
    #         x.download_video(item,p,i-1,p1)
    #         time.sleep(random.randint(5,10))
    # f.close()
   