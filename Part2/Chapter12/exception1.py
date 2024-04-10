def get_number():
    x = input("Enter a number: ")
    return int(x)

def main():
    while True:
        print(get_number() * 2)
        
main()
