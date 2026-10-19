password = (input("enter password: "))
password_length = len(password)
if password_length < 16:
    print("слишком короткий")
elif password.isalpha() == True or password.isdigit() == True:
    print("пароль слабый")
else:
    print("пароль надежный")