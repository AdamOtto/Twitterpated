import cx_Oracle
import pdb #debugger library
from functions import *

oracle_name = input("Please enter your oracle username: ")
oracle_pass = input("Please enter your oracle password: ")

try:
    con = cx_Oracle.connect(oracle_name,oracle_pass,"gwynne.cs.ualberta.ca:1521/CRS")
except:
    print("I'm sorry, but we couldn't make a connection to Oracle with those credentials")
    print("Exiting...")
    exit()

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
        #Clean the window and welcome the user
        clear_screen()
        print("Welcome to Twitterpated - the leading tweeting social network")
        print("What would you like to do?")
        print("1 - Login")
        print("2 - Register")
        print("3 - Exit")
        instr = get_valid_input(valids = ['1','2','3'])
        if instr is None or instr is '3':
            state = EXIT
        elif instr is '2':
            state = REGISTER
        elif instr is '1':
            state = LOGIN

    if state == LOGIN:
        user_login = login(cur)
        # infinite tries could make a limited amout
        while user_login[0] != 1 and user_login[0] != 2:
            user_login = login(cur)
        if user_login[0] == 1:
            while user_login[0] == LOGGED_IN:
                home_page(con, cur, user_login[1], user_login[2])
                functions(con, cur, user_login[1], user_login[2])
                state = WELCOME
                break
             
        elif user_login[0] == 2:
            state = WELCOME
        
        else:
            print("Login function error")

    elif state == REGISTER:
        if register(cur) == 1:
            con.commit()
            state = LOGIN
        #registration failed, present menu again
        state = WELCOME
            
cur.close()
con.close()         
