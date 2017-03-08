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
        while user_login[0] != 1 and user_login[0] != 2:
            user_login = login(cur)
        if user_login[0] == 1:
            while user_login[0] = LOGGED_IN
                home_page()
                functions()
                state = EXIT
                break
             
        elif user_login[0] == 2:
            state = WELCOME
        
        else
            print("Login function error")

    elif state == REGISTER:
        if register(cur) == 1:
            con.commit()
            state = LOGIN
            
cur.close()
con.close()         
