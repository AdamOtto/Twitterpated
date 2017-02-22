#State machine constants
EXIT = 0
WELCOME = 1
LOGIN = 2
REGISTER = 3

#start at the welcome screen
state = WELCOME

while state != EXIT:
    if state = WELCOME:
        print("Welcome to Twitterpated - the leading tweeting social network")
        print("What would you like to do?")
        print("1 - Login")
        print("2 - Register")
        print("3 - Exit")
        instr = getValidInput(['1','2','3'])
        if instr is None or instr is '3':
            state = EXIT
        elif instr is '2':
            state = REGISTER
        elif instr is '1':
            state = LOGIN



def getValidInput(valids, prompt = '', tries = Inf):
    """
    Will attempt to grab input from the user and check if it belongs to the
    passed list of valids, if not it will loop a maximum of tries times.
    prompt = str an initial prompt for user input, default ''
    valids = list of valid inputs
    tries = int of max loop amount, default 10

    returns input if valid input is found, otherwise None
    """
    attempt = 0
    while attempt < tries:
        print(prompt, end = '')
        instr = input()
        if instr in valid break
        print("That is not a valid input")
        attempt = attempt + 1
    if attempt >= tries:
        return None
    return instr
