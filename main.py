#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
import time
import traceback
from random import randint

from selenium import webdriver
from Queue import Queue
import threading

from captchar import capchar
from selenium.common.exceptions import TimeoutException
import select_solr_mc
from worker import parsemaininfo
NUM_WORKERS = 1
AVE_PAGES   = 20
i = 0
class MyThread(threading.Thread):
    def __init__(self, queue, i):
        self.queue = queue
        self.i = i
        # self._work_type
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                self.driver = webdriver.Firefox()
                if self.queue.qsize() > 0 and self.i < self.queue.qsize():
                    url = 'http://www.shuidixy.com/'
                    self.driver.get(url)
                    parsehtml(self.driver, self.queue, self.i)
                    self.i += 1
                else:
                    break
            except:
                time.sleep(randint(20*60, 30*60))

def parsehtml(driver, queue, i):
    nameend = queue.get()
    line = nameend.strip()
    name1 = line.decode('UTF-8-SIG')
    name2 = u"贵州"
    name = name2 + name1
    # name = u'北京京宁征信股份有限公司'
    try:
        clrinput = driver.find_element_by_id('searchkey')
        clrinput.clear()
        clrinput.send_keys(name)
        driver.find_element_by_id('searchBtn').click()

        nextclick = True

        links = []
        ipage = 1
        while nextclick:
            lists = driver.find_elements_by_xpath('//div[@class="or_search_list"]//a')
            for list in lists:
                companyname = list.text
                if select_solr_mc.search(companyname):
                    continue
                else:
                    link = list.get_attribute('href')
                    links.append(link)

            listInterests = driver.find_elements_by_xpath('div[@id="interestedCompany"]//a')
            for listInterest in listInterests:
                companyname = listInterest.text
                if select_solr_mc.search(companyname):
                    continue
                else:
                    links.append(listInterest)

            # lastindex = len(driver.window_handles)-1
            # driver.switch_to_window(driver.window_handles[lastindex])
            #c处理下一页
            try:
                nextpage = driver.find_element_by_xpath('//div[@class="sd_left-padge pageCls"]')
                # print nextpage.text
                nextpages = nextpage.find_elements_by_tag_name('span')
                # print nextpages[-1].text
                if nextpages[-1].text == u'下一页':
                    nextpages[-1].click()
                    time.sleep(randint(1, 2))
                    nextclick = True
                else:
                    nextclick = False
            except:
                # print traceback.print_exc()
                # time.sleep(40)
                nextclick = False

        print 'length of %d'% len(links)

        capchar(driver)
        print '------>'
        time.sleep(5)
        driver.quit()
        #去重
        ids = set(links)
        print len(ids)

        counterror = 0
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(20)
        for link in ids:
            print '[!]The company is %s' % name

            try:
                browser.get(link)
            except:
                browser.refresh()
                time.sleep(randint(10, 20))
            try:
                test = parsemaininfo(browser, name)
                if test:
                    counterror = 0
                    with open('errorlog.txt', 'w') as logfile:
                        logfile.write(str(counterror))
                else:
                    counterror += 1
                if counterror > 11:
                    time.sleep(randint(20*60, 40*60))

                    counterror = 0
                    with open('errorlog.txt', 'w') as logfile:
                        logfile.write(str(counterror))
            except:
                time.sleep(randint(10*20, 20*20))

        browser.quit()

        i = i + 1
        with open('log.txt', 'w') as logfile:
            logfile.write(str(i))
    except:
        driver.quit()
        print traceback.print_exc()

def crawl():
    queue = Queue()
    lines = open('3500.txt', 'r').readlines()
    try:
        with open('log.txt', 'r') as logfile:
            i = logfile.readline()
            i = int(i)
    except:
        i = 0
        pass
    for line in lines[i:]:
        queue.put(line)

    print queue.qsize()
    threads = []
    for x in range(NUM_WORKERS):
        thread = MyThread(queue, i)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    # print '%%%%%%%%%%%%'

if __name__ == '__main__':
    crawl()