money = int(input("how many money do you have? - ")) #поменять названия
hundreds = money // 100
temp = i*100
fifty = (money - temp) // 50
temp += j*50
ten = (money - temp) // 10
temp += k*10 
five = (money - temp) // 5
temp += l*5
two = (money - temp) // 2 
temp += m*2
one = (money - temp)
print("могу разменять на", hundreds, "по сто,", fifty, "по пятьдесят,", ten, 
      "по десять,", five, "по пять,", two, "монет по 2 рубля и", one, "по рублю" )