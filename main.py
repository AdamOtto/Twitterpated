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
        login_status = login(cur)
        # infinite tries could make a limited amout
        while login_status != 1:
            login_status = login(cur)
        if login_status == 1:
            functions(cur)
            #return

    elif state == REGISTER:
        if register(cur) == 1:
            con.commit()
            state = LOGIN

