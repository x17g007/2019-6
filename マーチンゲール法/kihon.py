import random
import collections
import statistics

motokin = 15800
haiboku = 0
kakesu = 72
loop = 1000
avg = 0
most_high = 0
tyuou = []
purasu = 0
mainasu = 0
hanbun = 0
bakueki = 0
onaji = 0
renAVG = 0
count = 0

for i in range(loop):
 syojikin = motokin
 kakekin = 100
 kakemoto = kakekin
 renzoku1 = 0
 renzoku2 = 0
 check = []
 kaisu = 0
 high = 0
 


 for i in range(kakesu):
   if(syojikin >= kakekin):
      num = random.randint(1,2)
      if(num == 2):
         syojikin = syojikin - kakekin
         kakekin = kakekin + kakekin
         #print("所持金は"+ str(syojikin) + "$です。賭け金は" + str(kakekin) + "$です。")
         renzoku1 = renzoku1 + 1
         if(renzoku1 > renzoku2):
            renzoku2 = renzoku1
                                                                     
      elif(num==1):
         syojikin = syojikin + kakekin
         kakekin = kakemoto
         #print("所持金は"+ str(syojikin) + "$です。賭け金は" + str(kakekin) + "$です。")
         renzoku1 = 0
      if(high <= syojikin):
         high = syojikin
      kaisu = kaisu + 1 
   else:
      break
   
   
 
 print("最大連続負け回数　　" + str(renzoku2))
 print("最高金額   " + str(high))
 print("最終金額   " + str(syojikin))
 print("------------------------------------")
 avg = avg + syojikin
 tyuou.append(syojikin)
 if(most_high < high):
    most_high = high
 if(motokin < syojikin):
    purasu = purasu + 1
    if(motokin * 1.5 < syojikin):
       bakueki = bakueki + 1
 elif(motokin > syojikin):
    mainasu = mainasu + 1
    if(motokin / 2 > syojikin):
       hanbun = hanbun + 1
 else:
    onaji = onaji +1
 renAVG = renAVG + renzoku2
 count = count + 1
print(str(motokin)+ "＄開始" )
print("最終金額平均は、" + str(avg/loop) + "$")
print("最高金額は" + str(most_high))
median = statistics.median(tyuou)
print("中央値は、" + str(median))
print("最大負け数平均は" + str(renAVG/loop))
print("増えた回数は、" + str(purasu) + "回、1.5倍増えた回数は、"+ str(bakueki) + "回")
print("減った回数は、" + str(mainasu) + "回、半分になった回数は、"+ str(hanbun) + "回、" + str((hanbun/loop)*100 )+ "％の確率で資金を半分以上失う")