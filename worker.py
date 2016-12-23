#encoding:utf-8

import time
import traceback
from random import randint

from sendall import sendall
def identity_zch(zch):
    zch_secend_number = zch
    print zch_secend_number
    zch_secend_number = int(zch_secend_number)
    if zch_secend_number == 11:
        province = u'北京'
        print province
        return province
    if zch_secend_number == 12:
        province = u'天津'
        return province
    if zch_secend_number == 13:
        province = u'河北'
        return province
    if zch_secend_number == 14:
        province = u'山西'
        return province
    if zch_secend_number == 15:
        province = u'内蒙'
        return province
    if zch_secend_number == 21:
        province = u'辽宁'
        return province
    if zch_secend_number == 22:
        province = u'吉林'
        return province
    if zch_secend_number == 23:
        province = u'黑龙江'
        return province
    if zch_secend_number == 31:
        province = u'上海'
        print province
        return province
    if zch_secend_number == 32:
        province = u'江苏'
        return province
    if zch_secend_number == 33:
        province = u'浙江'
        return province
    if zch_secend_number == 34:
        province = u'安徽'
        return province
    if zch_secend_number == 35:
        province = u'福建'
        return province
    if zch_secend_number == 36:
        province = u'江西'
        return province
    if zch_secend_number == 37:
        province = u'山东'
        return province
    if zch_secend_number == 41:
        province = u'河南'
        return province
    if zch_secend_number == 42:
        province = u'湖北'
        return province
    if zch_secend_number == 43:
        province = u'湖南'
        return province
    if zch_secend_number == 44:
        province = u'广东'
        return province
    if zch_secend_number == 45:
        province = u'广西'
        return province
    if zch_secend_number == 46:
        province = u'海南'
        return province
    if zch_secend_number == 50:
        province = u'重庆'
        return province
    if zch_secend_number == 51:
        province = u'四川'
        return province
    if zch_secend_number == 52:
        province = u'贵州'
        return province
    if zch_secend_number == 53:
        province = u'云南'
        return province
    if zch_secend_number == 54:
        province = u'西藏'
        return province
    if zch_secend_number == 61:
        province = u'陕西'
        return province
    if zch_secend_number == 62:
        province = u'甘肃'
        return province
    if zch_secend_number == 63:
        province = u'青海'
        return province
    if zch_secend_number == 64:
        province = u'宁夏'
        return province
    if zch_secend_number == 65:
        province = u'新疆'
        return province
def parsemaininfo(driver, name):
    try:
        qyxy = {}
        qygsgs = {}

        #基本信息
        jb = {}

        tbs = driver.find_elements_by_xpath('//div[@id="registerInfoTurnTo"]/div[2]//tr/*')
        print len(tbs)
        numBasic = len(tbs)
        iBasic = 0
        while iBasic < numBasic:
            key = tbs[iBasic].text.strip()
            value = tbs[iBasic + 1].text.strip()

            if u"企业信用代码" in key:
                if value == '':
                    pass
                else:
                    jb['zch'] = value
                    zch = jb['zch'][2:4]
                    area = identity_zch(zch)
            if u"注册号" in key:
                jb['zch'] = value
                zch = jb['zch'][:2]
                area = identity_zch(zch)
            # end if
            if u"类型" in key:
                jb['lx'] = value
            # end if
            # end if
            if u"法人代表" in key:
                jb['fr'] = value
            # end if
            if u"注册资本" in key:
                jb['zczb'] = value
            # end if
            if u"成立日期" in key:
                jb['clrq'] = value
            # end if
            if u"地址" in key:
                jb['zs'] = value
            # end if
            if u"登记机关" in key:
                jb['djjg'] = value
            # end if
            if u"核准日期" in key:
                jb['hzrq'] = value
            # end if
            if u"登记状态" in key:
                jb['djzt'] = value
            # end if
            if u"经营范围" in key:
                jb['jyfw'] = value
            # end if
            iBasic = iBasic + 2

        jb['mc'] = driver.find_element_by_id('company-status').text
        with open('ml.txt', 'a') as datefile:
            datefile.write(jb['mc'] + '\n')

        rq = driver.find_element_by_xpath('//*[@id="registerInfoTurnTo"]/div[2]/table/tbody/tr[4]/td[4]').text
        jb['jyqx1'] = rq[:10]
        jb['jyqx2'] = rq[13:]
        # end if

        jb['area'] = area
        print jb['area']
        jb['gxsj'] = time.time()
        qygsgs['jb'] = jb

        print qygsgs['jb']['zch']
        try:
            gd = []

            gdnextclick = True
            i = 1
            while gdnextclick:
                gdelements = driver.find_elements_by_class_name('partnerContentCls')

                for gdelement in gdelements:
                    elms = gdelement.find_elements_by_tag_name('td')
                    gd1 = {}
                    gd1['gd'] = elms[0].text
                    print gd1['gd']
                    gd1['rje'] = elms[1].text
                    if gd1['rje'] == '-':
                        gd1['rje'] = ''
                    gd.append(gd1)
                i += 1
                try:
                    bgnextpage = driver.find_element_by_xpath('//div[@id="partnerTurnTo"]/div[2]/div/p/span['+ str(i) + ']')
                    bgnextpage.click()
                    gdnextclick = True
                    time.sleep(randint(1, 2))
                except:
                    # print traceback.print_exc()
                    gdnextclick = False

            qygsgs['gd'] = gd
        except:
            print traceback.print_exc()

        try:
            zyry = []

            zyryelements = driver.find_elements_by_xpath('//div[@id="empListTurnTo"]/div[@class="panel_body"]/a')
            xh = 1
            for a in zyryelements:
                zyry1 = {}
                zyry1['xh'] = xh
                zyry1['xm'] = a.find_elements_by_tag_name('span')[0].text
                zyry1['zw'] = a.find_elements_by_tag_name('span')[1].text

                xh += 1
                zyry.append(zyry1)

            qygsgs['zyry'] = zyry
        except:
            print traceback.print_exc()

        try:
            bg = []
            nextclick = True
            i = 1
            while nextclick:
                bgelements = driver.find_elements_by_xpath('//div[@id="changeContent"]/div[@class="panel_jl_border"]')
                for bgelement in bgelements:
                    print bgelement.text
                    elms = bgelement.find_elements_by_tag_name('span')
                    bg1 = {}
                    bg1['bgsx'] = elms[0].text
                    bg1['bgrq'] = elms[2].text
                    bg1['bgqnr'] = elms[1].text
                    bg1['bghnr'] = elms[3].text
                    bg.append(bg1)

                i += 1
                try:
                    bgnextpage = driver.find_element_by_xpath('//div[@id="changeContent"]/div[@class="sd_left-padge pageCls"]/p/span['+ str(i) + ']')
                    bgnextpage.click()
                    nextclick = True
                    time.sleep(randint(1, 2))
                except:
                    # print traceback.print_exc()
                    nextclick = False

            qygsgs['bg'] = bg
        except:
            print traceback.print_exc()

        qyxy['qygsgs'] = qygsgs
        sendall(qyxy)

        return True
    except:
        return False