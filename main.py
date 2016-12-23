#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
import time
import traceback
from random import randint

from selenium import webdriver
from Queue import Queue
import threading

import select_solr_mc
from worker import parsemaininfo
NUM_WORKERS = 1
AVE_PAGES   = 20

class MyThread(threading.Thread):
    def __init__(self, queue):
        self.queue = queue
        # self._work_type
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                self.driver = webdriver.Firefox()
                if self.queue.qsize() > 0:
                    url = 'http://www.shuidixy.com/'
                    self.driver.get(url)
                    parsehtml(self.driver, self.queue)
                else:
                    break
            except:
                time.sleep(randint(20*60, 30*60))
def parsehtml(driver, queue):
    nameend = queue.get()
    line = nameend.strip()
    name1 = line.decode('UTF-8-SIG')
    name2 = u""
    name = name2 + name1

    print
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

        driver.quit()
        #去重
        ids = set(links)
        print len(ids)

        counterror = 0
        browser = webdriver.Firefox()
        for link in ids:
            print '[!]The company is %s' % name
            with open('errorlog.txt', 'w') as logfile:
                logfile.write(str(counterror))
            try:
                browser.get(link)
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
                time.sleep(10 * 60)
        browser.quit()
    except:
        print traceback.print_exc()

def crawl():
    queue = Queue()
    lines = open('3500.txt', 'r').readlines()
    for line in lines[101:]:
        queue.put(line)

    print queue.qsize()
    threads = []
    for x in range(NUM_WORKERS):
        thread = MyThread(queue)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    # print '%%%%%%%%%%%%'

if __name__ == '__main__':
    crawl()
