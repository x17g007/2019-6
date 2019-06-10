# -*- coding: utf-8 -*-
#たしかこれがメインで書いてたやつです
import pybitflyer
import time
from statistics import mean, median,variance,stdev

#初期化
midprice = 0
before_midprice = 0
before_mean = 0
pos = 0 # Long : 1, Short : -1, No position : 0
public_api = pybitflyer.API()
api = pybitflyer.API(api_key="WbENSqwxEDndU6cC8wKmob", api_secret="BLTT7N5u2b88XKPLqgXPGVJeF8gyW185VzQmYoKKG8s=")
#中間価格の初期化
midprice = before_midprice =  public_api.board(product_code = "FX_BTC_JPY")["mid_price"]

#条件式のための中間値配列
decision_price = []

#変数
array = 0
decision = 0
count = 0
test = 0
difference = 0

#ロング注文用のメソッド
def placeOrder_L(midprice):
    size = 1 # 枚数
    api.sendparentorder(order_method = "IFDOCO", 
                             parameters = [ 
                                 {"product_code":"FX_BTC_JPY", "condition_type":"MARKET","side" : "BUY" ,"size": size },
                                 
                                 {"product_code":"FX_BTC_JPY","condition_type":"LIMIT","side" : "SELL","price":midprice + 30,"size":size},
                                            
                                 {"product_code":"FX_BTC_JPY","condition_type":"STOP", "side" : "SELL","trigger_price":midprice - 60,"size": size}
                             ])

#ショート注文用のメソッド
def placeOrder_S(midprice):
    size = 1 # 枚数
    api.sendparentorder(order_method = "IFDOCO", 
                             parameters = [ 
                                 {"product_code":"FX_BTC_JPY", "condition_type":"MARKET","side" : "SELL" ,"size": size },
                                 
                                 {"product_code":"FX_BTC_JPY","condition_type":"LIMIT","side" : "BUY","price":midprice - 30,"size":size},
                                            
                                 {"product_code":"FX_BTC_JPY","condition_type":"STOP", "side" : "BUY","trigger_price":midprice + 60,"size": size}
                             ])


#ポジ入れてるか判別するメソッド
def pos_check(product_code):
    api.getpositions()
    



#メインループ
while True:
 time.sleep(0.1)
    #現在の中間価格を取得
 if array < 30:
        midprice = public_api.board(product_code = "FX_BTC_JPY")["mid_price"]
        decision_price.append(midprice)     #配列に価格を追加
        array = array + 1
        
        
        continue
 else:
        

        s = sum(decision_price)
        n = len(decision_price)
        mean = sum(decision_price) / len(decision_price) #平均算出
        print('平均:{0:.2f}'.format(mean))
        if test == 1:
            difference = mean - before_mean #差分
        print(difference)
        before_mean = mean
        decision = decision + difference
        if 10 < decision:
            decision = 0
            if pos == 0:
                pos = 1
        elif decision < -10:
            decision = 0
            if pos == 0:
                pos = -1
        else:
            count = count + 1
            if count == 20:
                print("decisionクリア！")
                count = 0
                decision = 0
        
    
        #決済注文
        if pos == 1:
            print("Long position")
            placeOrder_L(midprice)
            pos = 0
            continue
        elif pos == -1:
            print("Short position")
            placeOrder_S(midprice)
            pos = 0
            continue
       

        before_midprice = midprice # 価格をシフト
        decision_price.clear
        array = 0
        test = 1
        
    
