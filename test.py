def leap_year():
    check_year=int(input('Введите год: '))
    if check_year%400==0:
        return 'Високосный'
    elif check_year%100==0:
        return 'Невисокосный'
    elif check_year%4==0:
        return 'Високосный'
    else: 
        return 'Невисокосный'
    
print(leap_year())    
