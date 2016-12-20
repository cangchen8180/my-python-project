# coding=utf-8
import sys
import os
import csv
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')


def merge_xls(sheet, output_file, xlsdir):
    # outfile = open(output_file, "w")i
    with open(output_file, 'w') as csv_file:
        # spam_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spam_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        f_list = os.listdir('.')
        for f in f_list:
            if os.path.splitext(f)[1] == '.xls':
                xls = xlrd.open_workbook(f)
                sheet0 = xls.sheets()[0]
                rows = sheet0.nrows
                print 'file_name=', f
                print 'rows=', rows
                for i in range(rows):
                    if i > 1:
                        cells = sheet0.row_values(i)
                        spam_writer.writerow(cells)
                    # outfile.write(line)
                    # print "cell=", cell.encode('unicode_escape')


merge_xls(0, "result.csv", "")
