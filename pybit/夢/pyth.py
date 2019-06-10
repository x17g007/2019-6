#見てもよくわからないので、サンプルをもとに少しだけいじったものだと思う
import time
import pybitflyer
import requests
import datetime
import numpy as np

key = "" #BitFlyerの通常APIキー
secret = "" #BitFlyerのシークレットキー
bf = pybitflyer.API(key,secret)
product_code = "FX_BTC_JPY" #FX_BTC_JPYを対象とする
order_type   = "MARKET" #成り行き
soneki_per_sum = 0 #損益率
soneki = 0 #損益のsum
o = 0 #order関数を回った回数
j = 0 #一度目の注文タイミングは見送る変数
k= 1.645 #係数
kairi = 4.98 #価格乖離
period = 5 #期間
rev = 15 #レバリッジ
last_side = "" #最後に注文した方向
first_money = bf.getcollateral()["collateral"] #損益率を計算するために使用

#現在購入できるBTCの枚数を返す
def vol() :
	result_money = bf.getcollateral()
	ltp = get_ltp()
	money = np.floor(result_money["collateral"] - result_money["require_collateral"])
	size = money * rev / ltp
	return size

#保有している建玉数を計算
def get_pos() :
       size = 0
       poss = bf.getpositions(product_code=product_code)
       if len(poss) != 0:
           for pos in poss :
               size += pos["size"]
       return size

#過去2時間*期間分のデータを返す
def get_price(min) :
	price = []
	params = {"periods" : min }
	response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params)
	data = response.json()
	data["result"][str(min)].reverse()
	if data["result"][str(min)] is not None :
		i = 0
		for val in data["result"][str(min)] :
			if i < period + 1 :
				price.append([])
				price[i].append(val[2])#High
				price[i].append(val[3])#Low
				price[i].append(val[1])#Open_Price
			else :
				break
			i += 1
		return price
	else :
		print_log("データが存在しません")
		return None

#確定足のレンジ幅の平均値を返す
def get_ave(price_array) :
	ave_sum = 0
	del price_array[0]
	length = len(price_array)
	for price in price_array :
		ave_sum += price[0] - price[1]
	ave = ave_sum / length
	return ave

#形成中の足の始値を返す
def get_open(price_array) :
	return price_array[0][2]

#現物のltpを返す
def get_btc_ltp() :
    json = bf.ticker(product_code="BTC_JPY")
    return json["ltp"]

#FXのltpを返す
def get_ltp() :
    json = bf.ticker(product_code=product_code)
    return json["ltp"]

#注文処理を行う関数
def order(size,side) :
	global o
	global soneki
	global soneki_per_sum
	global first_money
	global kairi
	before_hyouka = bf.getcollateral()["collateral"]
	if o != 0 :
		size = round(get_pos(),2)
		u = 0
		while u == 0 :
			ltp_fx_price = get_ltp()
			ltp_btc_price = get_btc_ltp()
			diff = (ltp_fx_price / ltp_btc_price - 1) * 100
			if diff < kairi :
				u += 1
			if u == 0 :
				time.sleep(0.2)
		bf.sendchildorder(product_code=product_code, child_order_type=order_type, side=side, size=size)
		print("価格乖離： {0:.3f}%".format(diff))
		print("{0}BTCを{1}しました。".format(size,side))
		time.sleep(4)
		size = round(vol(), 2)
		u = 0
		while u == 0 :
			ltp_fx_price = get_ltp()
			ltp_btc_price = get_btc_ltp()
			diff = (ltp_fx_price / ltp_btc_price - 1) * 100
			if diff < kairi :
				u += 1
			if u == 0 :
				time.sleep(0.2)
		bf.sendchildorder(product_code=product_code, child_order_type=order_type, side=side, size=size)
		print("価格乖離： {0:.3f}%".format(diff))
		print("{0}BTCを{1}しました。".format(size,side))
		before_money = before_hyouka
		after_money = bf.getcollateral()["collateral"]
		print("{0} → {1}".format(before_money,after_money))
		money = after_money - before_money
		soneki += money
		soneki_per = money / after_money * 100
		if money > 0 :
			shouhai = "勝"
			money = "+" + str(money)
		elif money < 0 :
			shouhai = "負"
		else :
			shouhai = "引き分け"
		soneki_per_sum = soneki / first_money * 100
		print(money)
		print(shouhai)
		print("合計損益 ：{0:.0f}".format(soneki))
		print("損益率 ：{0:.2f}%".format(soneki_per))
		print("合計損益率 ：{0:.2f}%".format(soneki_per_sum))
	else :
		u = 0
		while u == 0 :
			ltp_fx_price = get_ltp()
			ltp_btc_price = get_btc_ltp()
			diff = (ltp_fx_price / ltp_btc_price - 1) * 100
			if diff < kairi :
				u += 1
			if u == 0 :
				time.sleep(0.2)
		bf.sendchildorder(product_code=product_code, child_order_type=order_type, side=side, size=size)
		print("価格乖離： {0:.3f}%".format(diff))
		print("{0}BTCを{1}しました。".format(size,side))
	time.sleep(2)
	o += 1

def main_process() :
	global k
	global last_side
	global j
	price = get_price(7200)
	ltp = get_ltp()
	ave = get_ave(price)
	open_price = get_open(price)
	if open_price + (k * ave) < ltp and last_side != "BUY":
		if j == 0 :
			last_side = "BUY"
			j += 1
		else :
			last_side = "BUY"
			size = vol()
			order(round(size, 2),last_side)
	if open_price - (k * ave) > ltp and last_side != "SELL" :
		if j == 0 :
			last_side = "SELL"
			j += 1
		else :
			last_side = "SELL"
			size = vol()
			order(round(size, 2),last_side)

#メイン処理
while True :
	i = 0
	pos = bf.getpositions(product_code=product_code)
	print('-----------------')
	while i < 4 :
		main_process()
		if pos != [] :
			pos_money = bf.getcollateral()["open_position_pnl"]
			print("評価損益 ：{0:.0f}".format(pos_money))
		time.sleep(7)
		i += 1
