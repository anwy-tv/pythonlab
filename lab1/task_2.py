password = (input("enter password: "))
password_length = len(password)
if password_length < 16:
    print("пароль слишком короткий")
elif password.isalpha() == True:
    print("пароль слабый")
elif password.isdigit() == True:
    print("пароль слабый")
elif password.isalpha() != True and password.isdigit() != True and password.islower() == True:
    print("пароль слабый")
elif password.isalpha() != True and password.isdigit() != True and password.islower() != True:
    print("пароль надежный")
