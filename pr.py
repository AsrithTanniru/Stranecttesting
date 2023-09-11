def sum(a,b):
    if type(a) == int and type(b) == int :
        sum = a + b
        print(sum)
        return sum
    else:
        print("please input only integers")

        return False
    

sum("fvf",2)