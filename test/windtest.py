from WindPy import w
import sys


def connection_wind():
    w.start()
    print('\n\n' + '-----通过wsd来提取各个报告期财务数据-----' + '\n')
    wsddata2 = w.wsd("600000.SH", "tot_oper_rev,tot_oper_cost,opprofit,net_profit_is", "2008-01-01", "2015-12-22",
                     "rptType=1;Period=Q;Days=Alldays;Fill=Previous")
    print(wsddata2)


if __name__ == '__main__':
    connection_wind()
