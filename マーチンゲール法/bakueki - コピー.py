import random
import collections
import statistics

#1セット30秒かかる計算で、2時間プレイとしたので、240回
#賭け金は気合出してせいぜい5万円=450＄
motokin = 300
mokuhyou = 16000 #資産
haiboku = 0
loop = 1000 
avg = 0
most_high = 0
purasu = 0
mainasu = 0
hanbun = 0
bakueki = 0
count = 0

for i in range(loop):
 syojikin = motokin
 kakekin = 5 #一度の賭け金
 kakemoto = kakekin
 renzoku1 = 0
 renzoku2 = 0
 check = []
 kaisu = 0
 high = 0
 while(syojikin < mokuhyou):
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
        if(renzoku1 > 5):
            check.append(renzoku1)
        renzoku1 = 0
    kaisu = kaisu + 1 
    if(high < syojikin):
        high = syojikin
    if(syojikin < kakekin):
        break
   
 print("最大連続負け回数　　" + str(renzoku2))
 print("最高金額   " + str(high))
 print("最終金額   " + str(syojikin))
 print("------------------------------------")
 if(high >= mokuhyou):
     count = count + 1
 avg = avg + syojikin
 if(most_high < high):
    most_high = high
 if(motokin < syojikin):
    purasu = purasu + 1
    if(motokin * 1.2 < syojikin):
       bakueki = bakueki + 1
 elif(motokin > syojikin):
    mainasu = mainasu + 1
    if(motokin / 2 > syojikin):
       hanbun = hanbun + 1
print("最終金額平均は、" + str(avg/loop) + "$")
print("最高金額は" + str(most_high))
print("増えた回数は、" + str(purasu))
print("減った回数は、" + str(mainasu) + "回、半分になった回数は、"+ str(hanbun) + "回")
print("勝率は" + str((purasu/loop)*100)+ "％")
print("目標達成回数は" + str(count) + "回")