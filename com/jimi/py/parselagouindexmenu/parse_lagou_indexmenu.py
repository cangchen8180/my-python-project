# coding=utf-8
import sys
import csv
import urllib2
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

response = urllib2.urlopen("http://www.lagou.com")
lg_index = response.read()
# print lg_index
lg_index_soup = BeautifulSoup(lg_index, 'html.parser')
print 'original_code=', lg_index_soup.original_encoding

outfile = open("result.csv", 'w')
csv_wt = csv.writer(outfile, delimiter=',')

for main_menu_div in lg_index_soup.find_all("div", class_="menu_box"):
    main_menu_name = main_menu_div.find("h2").get_text()
    # main_menu_name = ''.join(main_menu_name.split(' '))
    # 一次性去除空白字符、空白行等
    main_menu_name = main_menu_name.strip(' \t\n\r')
    print '--', main_menu_name
    for sub_menu_dl in main_menu_div.find_all('dl'):
        sub_menu_name = sub_menu_dl.find('dt').a.string
        print '  --', sub_menu_name
        for third_menu in sub_menu_dl.find('dd').find_all('a'):
            third_menu_name = third_menu.string
            print '    --', third_menu_name
            csv_wt.writerow([main_menu_name, sub_menu_name, third_menu_name])

outfile.close