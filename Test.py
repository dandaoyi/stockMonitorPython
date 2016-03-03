__author__ = 'huaxz'
from Monitor import  Monitor
import StockList
import time
M=Monitor()
shList=['sh'+item for item in StockList.shStockList]
szList=['sz'+item for item in StockList.szStockList]
stocklist= shList+szList
#开始遍历
while True:
    temp=M.monitor(stocklist)
    time.sleep(3)

