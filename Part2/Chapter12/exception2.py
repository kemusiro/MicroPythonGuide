def get_number():
    x = input("Enter a number: ")
    return int(x)

def main():
    while True:
        try:
            print(get_number() * 2)
        except ValueError as e:
            print(e)
        
main()
