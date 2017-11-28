z = 6
while True:
    if z == 5:
        print("first loop active")
        print("doing stuff in first loop")
        while True:
            print("second loop active")
            print("doing stuff in 2nd loop")
            break
        break
    else:
        print("z does satisfy the condition")



