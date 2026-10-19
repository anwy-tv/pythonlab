money = int(input("how many money do you have? - "))
i = money // 100
temp = i*100
j = (money - temp) // 50
temp += j*50
k = (money - temp) // 10
temp += k*10 
l = (money - temp) // 5
temp += l*5
m = (money - temp) // 2 
temp += m*2
n = (money - temp)
print("могу разменять на", i, "по сто,", j, "по пятьдесят,", k, 
      "по десять,", l, "по пять,", m, "монет по 2 рубля и", n, "по рублю" )

print ("или")
j = money//50
k = money//10
l = money//5
m = money//2
print ("могу разменять на", i, "по сто,", j, "по пятьдесят,", k,
        "по десять,", l, "по пять,", m, "монет по 2 рубля и", money, "по рублю без сдачи :)" )