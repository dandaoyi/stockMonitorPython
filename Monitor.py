__author__ = 'huaxz'
import urllib.request
import time
import urllib.parse
import winsound
def play():
    winsound.PlaySound('SystemQuestion', winsound.SND_ALIAS) #立即返回，支持异步播放
lastQuote={}#时间标记
class Monitor:
#http://hq.sinajs.cn/list=sh601003,sh601001
    URL='http://hq.sinajs.cn/list=%s'
    def monitor(self,stockListWithMarket):
        stockCode=','.join(stockListWithMarket)
        html=self.__getHtml(stockCode)
        result=self.__parse(html)
        return result
    def __getHtml(self,stockCode):
        request=urllib.request.Request(Monitor.URL%stockCode)
        request.add_header('accept-encoding','deflate')
        response = urllib.request.urlopen(request)
        content=response.read().decode('gbk','ignore')#遇到非法字符则忽略
        return content.strip()
    def __parse(self,txt):
        dataList=txt.split(';')
        result=[]
        for item in dataList:
            if item:
                temp=self.__parseItem(item)
                if temp:
                    result.append(temp)
        return result
    def __parseItem(self,item):
        dataList=item.split('"')
        code=dataList[0][-7:-1]
        data=dataList[1]
        stockData=data.split(',')
        result={
            'stockCode':code,#股票代码
            'vol':stockData[8],#当日成交量（股）
            'buyV1':stockData[10],#买一量（股）
            'buyV2':stockData[12],#买二量（股）
            'buyV3':stockData[14],#买三量（股）
            'buyV4':stockData[16],#买四量（股）
            'buyV5':stockData[18],#买五量（股）
            'sellV1':stockData[20],#卖一量（股）
            'sellV2':stockData[22],#卖二量（股）
            'sellV3':stockData[24],#卖三量（股）
            'sellV4':stockData[26],#卖四量（股）
            'sellV5':stockData[28],#卖五量（股）
            'time':stockData[31]#时间
        }
        global lastQuote
        if(code in lastQuote) and stockData[31]<=lastQuote[code]['time']: #未更新
            return None
        else:#开始更新            
            if code in lastQuote:
                last=lastQuote[code]#上一个记录
                totalSell=result['sellV1']+result['sellV2']+result['sellV3']+result['sellV4']+result['sellV5']#卖五量
                if totalSell>0:
                    play()
                    print('\t\t%s:%s已开板'%(result['time'],result['stockCode']))
                else:
                    totalBuy=result['buyV1']+result['buyV2']+result['buyV3']+result['buyV4']+result['buyV5']#买五量
                    lastTotalBuy=last['buyV1']+last['buyV2']+last['buyV3']+last['buyV4']+last['buyV5']#上一次买五量
                    minusBuy=lastTotalBuy-totalBuy #买五减少量
                    if minusBuy/lastTotalBuy >0.2:#减少20%则提示
                        play()
                        print('\t\t%s:%s涨停板被砸'%(result['time'],result['stockCode']))
            lastQuote[code]=result#更新最新事件
            return result

