import random


MAX_LINES = 3    #Global Constant: all caps as its a constant value and its not going to change
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3



symbol_count = {
    "🤑": 2,
    "💰": 4, 
    "💵": 6,
    "🪙": 8
}

symbol_value = {
    "🤑": 5,
    "💰": 4,
    "💵": 3,
    "🪙": 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:                                         #what this else statement will do, is tell us if we didn't break out of for loop. If we break the else doesn't run,  if no break the else runs.
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    
    return winnings, winning_lines




def get_slot_machine_spin(rows, cols, symbols):       #generation of items in our slot machine
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):                 #use "_" its an anoymous variable in Python, whenever you wanna loop through something but dont care about count or iteration value then use "_" so you dont have an unused variable
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]              # we dont want a reference we want a copy, so thats why we use "[:]"
        for _ in range(rows):
            value = random.choice(all_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)
    
    return columns

def print_slot_machine(columns):                            #transposing 
    for row in range(len(columns[0])):                      #assumes we have atleast 1 column
        for i, column in enumerate(columns):                #enumerate gives us index as well as the item
            if i != len(columns) - 1:
                print(column[row], end=" | ")                     # " | " pipe operator if not at the end 
            else:
                print(column[row], end="")

        print() #prints new line character, and then goes to next row


def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0!")
        else:
            print("Please enter a valid number")
    return amount 

last_lines = None
last_bet = None

def get_number_of_lines():
    global last_lines
    while True:
        lines = input("Enter the number of lines you would like to bet on (1-" + str(MAX_LINES) + ")? ") #adds MAX_LINES as a string 
        if lines.isdigit():
            lines = int(lines)
        if 1 <= lines <= MAX_LINES:
            last_lines = lines       #Saves previous line selection
            break
        else:
            print("Lines must be greater than 0!")
    return lines 

def get_bet():
    global last_bet
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
        if MIN_BET <= amount <= MAX_BET:
            last_bet = amount        #Saves previous bet selection
            break
        else:
            print(f"Bet must be between ${MIN_BET} - ${MAX_BET}")
    return amount 


def spin(balance):
    global last_lines, last_bet
    if last_lines is not None and last_bet is not None:
        replay = input("Press 'r' to replay your last spin or 'n' to make a new bet: ")
        if replay.lower() == 'r':
            lines = last_lines
            bet = last_bet
        else:
            lines = get_number_of_lines()
            bet = get_bet()
    else:
        lines = get_number_of_lines()
        bet = get_bet()

    total_bet = bet * lines
    
    while total_bet > balance:
        print(f"You do not have enough funds to place that bet, your current balance is: ${balance}")
        lines = get_number_of_lines()
        bet = get_bet()
        total_bet = bet * lines

    print(f"You are betting ${bet} on {lines} lines. Your Total bet is equal to: ${total_bet} per spin.")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on line(s):", *winning_lines)    #splat / unpack operator , gonna pass every single line from winning_lines to the print function. 

    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"Current Balance is: ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
    
    print(f"You left with ${balance}")



main()
