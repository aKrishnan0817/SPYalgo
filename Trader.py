import pandas as pd
import time
from datetime import datetime
import pickle

class Trader:
    def __init__(self):
        self.tradeData = pd.DataFrame(dict(Position = [],TradePrice = [], TradeTime = []))

    def goLong(self,currTimeRow):
        price = currTimeRow["price"]
        time = currTimeRow["Time2"]
        self.tradeData = pd.concat([self.tradeData, pd.DataFrame([[1,price,time]], columns=self.tradeData.columns) ], ignore_index=True)

    def goShort(self,currTimeRow):
        price = currTimeRow["price"]
        time = currTimeRow["Time2"]
        self.tradeData = pd.concat([self.tradeData, pd.DataFrame([[-1,price,time]], columns=self.tradeData.columns) ], ignore_index=True)

    def closeOut(self,currTimeRow):
        price = currTimeRow["price"]
        time = currTimeRow["Time2"]
        self.tradeData = pd.concat([self.tradeData, pd.DataFrame([[0,price,time]], columns=self.tradeData.columns) ], ignore_index=True)

    def getTradeData(self):
        return self.tradeData

    def getReturnList(self,contractValue=50):
        ReturnList =[]
        for i in range(0,len(self.tradeData)):
            if self.tradeData.loc[i,'Position'] == -1:
                ReturnList.append((self.tradeData.loc[i,'TradePrice']-self.tradeData.loc[i+1,'TradePrice'])*contractValue)
            elif self.tradeData.loc[i,'Position'] == 1:
                ReturnList.append((self.tradeData.loc[i + 1, 'TradePrice']-self.tradeData.loc[i, 'TradePrice'])*contractValue)
        return ReturnList

    def getTradeInfo(self,contractValue=50):
        ReturnList = self.getReturnList(contractValue)
        return {"Total Return" :sum(ReturnList),
                "Max Return" : max(ReturnList),
                "Min Return" : min(ReturnList)}
