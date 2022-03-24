import gbnclientapp
#import ricardo sr client app

def main():
    print("Please select between \n 1) Go-back-N \n 2)Selective Repeat")
    selection = input(">")

    if selection == 1:
        gbnclientapp.main()

    elif selection == 2:
        #sr server app main
        pass
    else:
        print("please make a valid selection")

if __name__ == '__main__':
    main()