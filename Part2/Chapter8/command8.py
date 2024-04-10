message = "Good morning!"

def change_message(m):
    global message
    message = m
    
def print_message():
    print(message)
    
print_message()
change_message("Good afternoon!")
print_message()