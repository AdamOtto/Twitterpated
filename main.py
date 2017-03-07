import cx_Oracle
import pdb #debugger library
from functions import *
con = cx_Oracle.connect("crapo","3sidedpolygon","gwynne.cs.ualberta.ca:1521/CRS")
cur = con.cursor()

#State machine constants
EXIT = 0
WELCOME = 1
LOGIN = 2
REGISTER = 3

#start at the welcome screen
state = WELCOME

#user_login constants
LOGGED_IN = 1
NO_LOGIN = 0

#Initialize the login information
#(logged in boolean, user id, name)
user_login = (NO_LOGIN, None, None)

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
        user_login = login(cur)
        # infinite tries could make a limited amout
        while user_login(0) != 1:
            user_login = login(cur)
        if user_login(0) == 1:
            while user_login(0) = LOGGED_IN
                home_page()
        elif
            print("Login function error")

    elif state == REGISTER:
        if register(cur) == 1:
            con.commit()
            state = LOGIN

            
def home_page()
'''
Provides the opening homepage for initial user login. It explains
some controls, and displays tweets of followed users 5 at a time.
There is an option to go and use the program functions for more
advanced usage.
'''
    print("Welcome to Twitterpated! Here are all your followed users' tweets:")
    # @TODO need to get both tweets and retweets
    cur.execute("select tid, writer, usr, tdate, text, replyto " +
                "from tweets t, users u " +
                "where t1.writer = u1.usr " + 
                "union " + 
                "select tid, writer, usr, rdate, text " + 
                "from retweets r join users u1 on r. users u2, )


# Provides a menu for the functions of the program
def functions():
    print("Welcome to Twitterpated! The functions of Twitterpated are listed below.")

    print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
          "Tweet\n 4 - List Followers\n5 - Manage Lists\n6 - Logout")
    f_input = input("What would you like to do? ")

    while f_input:
        if f_input == "1":
            search_tweet(cur)
        elif f_input == "2":
            search_user(cur)
        elif f_input == "3":
            write_tweet(cur, user_login)
        elif f_input == "4":
            list_followers(cur)
        elif f_input == "5":
            manage_lists(cur)
        elif f_input == "6":
            print("Logging out of Twitterpated.")
            return 1
        else:
            print("The input entered was not valid. Please enter one of specified prompts.")

        print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
              "Tweet\n 4 - List Followers\n5 - Manage Lists\n6 - Logout")
        f_input = input("What would you like to do? ")

    return 1