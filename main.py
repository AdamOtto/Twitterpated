import cx_Oracle
con = cx_Oracle.connect("username","password","gwynne.cs.ualberta.ca:1521/CRS")
cur = con.cursor()

#State machine constants
EXIT = 0
WELCOME = 1
LOGIN = 2
REGISTER = 3

#start at the welcome screen
state = WELCOME

while state != EXIT:
    if state == WELCOME:
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
                  
if state == LOGIN:
    login()
elif state == REGISTER:
    register()


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
        if instr in valid: break
        print("That is not a valid input")
        attempt = attempt + 1
    if attempt >= tries:
        return None
    return instr

# if login is specified gets the users id and password and checks to see if the user is
#  in the table, returning 1 if they are 0 if they are not
def login():
    userID = input("Please enter your user ID: ")
    pswd = input("Please enter your password: ")
    
    cur.execute("select name from users where usr = userID and pwd = pswd")
    
    name = cur.fetchall()
    if name:
        print("Welcome to Twitterpated ", name, "!")
        return 1
    else:
        return 0

# if register is specified prompts the user for all the information to create a user in the table
def register():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    city = input("Enter the city you live in: ")
    timezone = input("Enter your timezone: ")
    float(timezone)
    pswd = input("Enter your password: ")
    # need to add error checking to all of these to make sure correct information is entered 
    #  and maybe a better prompt to specify conditions 
    
    user = ("select max(usr) from users")
    int(user)
    user = user + 1
    cur.execute("insert into user values(usr,pswd,name,email,city,timezone)")
    print(name, " your user ID is ", usr, ", don't forget this as it is used to login.")
    print("Thank you for registering with Twitterpated!")
    return 1
    
