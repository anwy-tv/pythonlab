money = int(input("how many money do you have? - ")) #поменять названия
hundreds = money // 100
temp = hundreds*100
fifty = (money - temp) // 50
temp += fifty*50
ten = (money - temp) // 10
temp += ten*10 
five = (money - temp) // 5
temp += five*5
two = (money - temp) // 2 
temp += two*2
one = (money - temp)
print("могу разменять на", hundreds, "по сто,", fifty, "по пятьдесят,", ten, 
      "по десять,", five, "по пять,", two, "монет по 2 рубля и", one, "по рублю" )