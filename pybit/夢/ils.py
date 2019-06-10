import time
import pybitflyer
import requests
import datetime
import numpy as np

key = ""	#Bitflyerの通常APIキー
secret = "" #Bitflyerのシークレットキー
bf = pybitflyer.API(key.secret)
product_code = "FX_BTC_JPY" #FX_BTCを指定
order_type = "MARKET" #成行
soneki_per_sum = 0 #損益率
soneki = 0 #損益のsum
period = 5
rev = 15
last_side = "" #最後に注文した方向
first_money = bf.getcollateral()["collateral"] #損益率を計算する為に使用

#現在購入できるBTCの枚数を返す
def vol() :
	result_money = bf.getcollateral()
	ltp = get_ltp()
	money = np.floor(result_money["collateral"] - result_money["require_collateral"])
	size = money * rev / ltp
	return size

#保有している建玉数を計算
def get_pos()
        size = 0
        poss = bf.getpositions(product_code = product_code)
        if len(poss) != 0:
           for pos in poss:
                size +=pos["size"]
        return size

#過去X時間分のデータを返す
def get_price(min) :
	price = []
	params = {"periods" : min}
	response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params)
	data = response.json()
	data["result"][str(min)].reverse()
	if data["result"][str(min)] is not None :
		i = 0
		for val in data["result"][str(min)] :
			if i < period + 1
				price.append([])
				price[i].append(val[2])#High
				price[i].append(val[3])#Low
				price[i].append(val[1])#Open_price
			else:
				break
			i += 1
		return price
	else :
		print_log("データが存在しません")
		return None
		
#確定足のレンジ幅の平均値を返す
def get_ave(price_array)
	ave_sum = 0
	del price_array[0]
	length = len(price_array) :
	for price in price_array
		ave_sum += price[0] - price[1]		
	ave = ave_sum / length
	return ave
	
#形成中の足の始値を返す
def get_open(price_array) :
	return price_array[0][2]


#注文処理を行う関数
def order(size,side) :
	global o
	global soneki
	global soneki_per_sum
	global first_money
	before_hyouka = bf.getcollateral()["collateral"]
	if o ! = 0 :
		size = round(get_pos(),2)
		######ここにループIFD######
		print("{0}BTCを{1}しました。".format(size,side))
		time.sleep(4)
		size = round(vol(),2)
		#####ここにループIFD#####
		print("{0}BTCを{1}しました。".format(size,side))
		before_money = bofore_hyouka
		after_money = bf.getcollaterral()["collateral"]
		print("{0} → {1}".format(bofore_money,after_money))
		money = after_money - before_money
		soneki += money
		soneki_per = money / after_money * 100
		if money > 0 :
			syouhai = "勝"
			money = "+" + str(money)
		elif money < 0 :
			syouhai = "負"
		else :
			syouhai = "引き分け"
		soneki_per_sum= soneki / first_money * 100
		print(money)
		print(shouhai)
		print("合計損益 : {0:.0f}".format(soneki))
		print("損益率 : {0:.2f}%".format(soneki_per))
		print("合計損益率 : {0:.2f}%".format(soneki_per_sum))
	
		
		
		
		
		
			

	
	
			
	
