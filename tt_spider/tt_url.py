__author__ = 'icepros'
# coding=utf-8
from selenium import webdriver
import codecs
import threading
import time
import threadpool

threadLock = threading.Lock()
file = codecs.open('/home/icepros/logback/tt.txt', 'wb', encoding='utf-8')


def tiantuan_spider(counter):
    get_url = "http://tuan.zhiuxing.com:9999/"
    while counter:
        driver = webdriver.PhantomJS()
        # driver = webdriver.Chrome()
        driver.get(get_url)
        driver.implicitly_wait(2)
        urls = []
        try:
            links = driver.find_elements_by_tag_name("a")

            for link in links:
                url = str(link.get_attribute('href'))
                link_name = link.text
                if url.find('tuan.zhiuxing.com:9999') != -1:
                    urls.append(url)
                    threadLock.acquire()
                    file.write(u"链接名称:%s;     链接:%s" % (link_name, url) + "\n")
                    threadLock.release()

            for u in urls:
                driver.get(u)
                print u

        finally:
            driver.delete_cookie('foo')
            driver.close()

        counter -= 1


# 模拟 driver 数
def my_driver():
    counters = []
    for c in range(1, 1000):
        counters.append(c)
    return counters


i = my_driver()

if __name__ == "__main__":
    # 使用多线程执行telnet函数
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(tiantuan_spider, i)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    file.close()
