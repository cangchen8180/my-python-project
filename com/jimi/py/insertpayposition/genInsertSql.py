# coding=utf-8
import string
import sys
import os
import csv
import urllib2
from bs4 import BeautifulSoup
import time
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')


def handle(input_f, output_f):
    # outs = []
    optf = open(output_f, 'wb')
    wr = csv.writer(optf, delimiter=';', quoting=csv.QUOTE_MINIMAL, quotechar=' ')

    # 使用with as
    # 类似try..except这种异常处理机制， 其实就是不用调用file.close方法了
    with open(input_f, 'rb') as iptf:
        rows = csv.reader(iptf)
        orderNo_prefix = "cs_" + time.strftime("%Y%m%d", time.localtime()) + ""

        index = 0
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for row in rows:
            index += 1
            columns = row[0].split()
            cmpId = columns[0]
            positionId = columns[1]
            positionType = ''
            size = len(columns)
            if size >= 3:
                positionType = columns[2]
            sale = ''
            if size >= 4:
                sale = columns[3]

            # 爬主站获取公司logo
            company_url = "https://www.lagou.com/gongsi/{}.html".format(cmpId)
            logo_url = get_company_logo_from_html(company_url)
            # print logo_url

            order_no = orderNo_prefix + str(index)

            # 单引号 方式
            # sql_m = 'INSERT INTO `lagou_activity`.`pay_position_record` ' \
            #         '(`activityType`, `orderNo`, `companyId`, `positionId`, `positionType`, `payUserName`, `portrait`,' \
            #         '`userId`, `userType`, `payPhone`, `productSlug`, `source`, `status`, `remark`, `updateTime`, `createTime`) ' \
            #         'VALUES (\'ACTIVITY\',' \
            #         ' \'{}\', {}, {}, \'{}\',\'{}\', \'{}\', 0, \'B\', \'18622761111\',\'yiyuanduobao\', \'\', \'\', \'手动生成订单，未对接到支付系统\',' \
            #         '\'2016-12-15 17:10:38\', \'2016-12-15 17:10:40\');'.format(order_no, cmpId, positionId, positionType,
            #                                                                 sale, logo_url)

            # 双引号 方式
            # sql_m = "INSERT INTO `lagou_activity`.`pay_position_record` " \
            #          "(`activityType`, `orderNo`, `companyId`, `positionId`, `positionType`, `payUserName`, `portrait`," \
            #          "`userId`, `userType`, `payPhone`, `productSlug`, `source`, `status`, `remark`, `updateTime`, `createTime`) " \
            #          "VALUES ('ACTIVITY'," \
            #          "'{}', {}, {}, '{}','{}', '{}', 0, 'B', '18622761111','yiyuanduobao', '', '', '手动生成订单，未对接到支付系统'," \
            #          "'2016-12-15 17:10:38', '2016-12-15 17:10:40');".format(order_no, cmpId, positionId, positionType,
            #                                                                  sale, logo_url)

            # 三引号 块方式
            # 使用mybatis执行sql
            # sql_for_code = """INSERT INTO pay_position_record (activityType, orderNo, companyId, positionId, positionType, payUserName, portrait, userId, userType, payPhone, productSlug, source, status, remark, updateTime, createTime) VALUES ('ACTIVITY', '{}', {}, {}, '{}','{}', '{}', 0, 'B', '18622761111','yiyuanduobao', '', '', '手动生成订单，未对接到支付系统', '{}', '{}');"""\
            #     .format(order_no, cmpId, positionId, positionType, sale, logo_url, nowTime, nowTime)


            # 三引号 块方式
            # 运维手动执行的sql
            sql_m = """INSERT INTO `lagou_activity`.`pay_position_record` (`activityType`, `orderNo`, `companyId`, `positionId`, `positionType`, `payUserName`, `portrait`, `userId`, `userType`, `payPhone`, `productSlug`, `source`, `status`, `remark`, `updateTime`, `createTime`) VALUES ('ACTIVITY', '{}', {}, {}, '{}','{}', '{}', 0, 'B', '18622761111','yiyuanduobao', '', '', '手动生成订单，未对接到支付系统', '{}', '{}');""" \
                .format(order_no, cmpId, positionId, positionType, sale, logo_url, nowTime, nowTime)

            print order_no
            # outs.append(sql_m)
            wr.writerow([sql_m])
            # 打印数据方式
            # print "compId=%s, pid=%s, ptype=%s, sale=%s" %(cmpId, positionId, positionType, sale)

    optf.close()


# 获取指定公司的logo地址
def get_company_logo_from_html(company_url):
    resp = urllib2.urlopen(company_url)
    company_page = BeautifulSoup(resp.read(), "html.parser")
    logo_div = company_page.find("div", class_="top_info_wrap")
    logo_url = "https:" + logo_div.find("img").get("src")
    return logo_url


def printTime():
    # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time.strftime("%Y%m%d", time.localtime())


def genSqlFileName():
    return "insert_sql_" + printTime() + ".sql"


# printTime()
handle("data.csv", genSqlFileName())
# get_company_logo_from_html("https://www.lagou.com/gongsi/1880.html")
