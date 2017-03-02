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
        login_status = login()
        # infinite tries could make a limited amout
        while login_status != 1:
            login_status = login()
        if login_status == 1:
            functions()
            #return

    elif state == REGISTER:
        if register() == 1:
            if login() == 1:
                functions()
                #return


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


    # Provides a menu for the functions of the program
    def functions():
        print("Welcome to Twitterpated! The functions of Twitterpated are listed below.")

        print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
              "Tweet\n 4 - List Followers\n5 - Manage Lists\n6 - Logout")
        f_input = input("What would you like to do? ")

        while f_input:
            if f_input == "1":
                search_tweet()
            elif f_input == "2":
                search_user()
            elif f_input == "3":
                write_tweet()
            elif f_input == "4":
                list_followers()
            elif f_input == "5":
                manage_lists()
            elif f_input == "6":
                print("Logging out of Twitterpated.")
                return 1
            else:
                print("The input entered was not valid. Please enter one of specified prompts.")

            print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
                  "Tweet\n 4 - List Followers\n5 - Manage Lists\n6 - Logout")
            f_input = input("What would you like to do? ")

        return 1

# prompts the user to enter a keyword to be searched for in tweets and prints
#  ou the top 5 recent tweets and gives the user the option to select a tweet
#  and get some stats about it or recieve the next 5 tweets.
def search_tweet():
    keyword = input("Please enter the keyword(s) you would like search. (If you"
                    " are entering more than one keyword, please seperate using"
                    " a ','): ")

    keyword.split(',')
    for word in keyword:
        word.strip()
        cur.execute("select text from "
                    "(select text, row_number(order by tdate descending) as row_num "
                    "from tweets where text like '%word%') where row_num <= 5")
        tweets = cur.fetchall()
        index = 1
        for tweet in tweets:
            print(index, " ", tweet)
            index += 1
        if index > 5:
            more_tweets = input("Would you like to receive the next 5 tweets "
                                "with the matching keyword from before? Enter "
                                "yes or no: ")
            while (more_tweets == 'yes'):
                cur.execute("select text from "
                            "(select text, row_number(order by tdate descending) as row_num "
                            "from tweets where text like '%word%') where row_num <= 5")
                #not finished

    return

def search_user():
    return

def write_tweet():
    return

def list_followers():
    return

def manage_lists():
    return
