import pdb
import queries
import os

CLEAR_SCREEN = 'cls' if os.name == 'nt' else 'clear'

def get_valid_input(length = 20, valids = [], valids_description = None, prompt = '', tries = float('inf')):
    """
    Will attempt to grab input from the user and check if it belongs to the
    passed list of valids, if not it will loop a maximum of tries times.
    length = max input length
    valids = list of valid inputs, optional, if left blank only checks against length
    valids_description = a description of the valids that is used to help a user if they input something invalid, default None
    prompt = str an initial prompt for user input, default ''
    tries = int of max loop amount, default infinite, if tries exceed and no input given, returns none
    
    returns input if valid input is found, otherwise None
    """
    attempt = 0
    while attempt < tries:
        attempt = attempt +1
        instr = input(prompt)
        #Length check first
        if len(instr) > length:
            print("That input is too long, the max is " + str(length) + " chars long")
            continue
        #Valids check if applicable
        if valids != []:
            if instr in valids:
                break
            print("That is not a valid input (", end = '')
            print(*valids, end = '') if valids_description is None else print(valids_description, end = '')
            print(")")
        else:
            break
    if attempt >= tries:
        return None
    return instr


# if login is specified gets the users id and password and checks to see if the user is
#  in the table, returning 1 if they are 0 if they are not
def login(cur):
    userID = input("Please enter your user ID (Enter nothing to return to menu): ")
    if not userID:
        print("Returning to menu.")
        return(2, None, None)
    
    if (userID.isdigit()):
        query = "select * from users where usr = :ID"
        cur.execute(query, {'ID':int(userID)})
        user_info = cur.fetchall()
    else:
        print("Your user ID needs to be number.")
        return (0, None, None)
    
  #  print(user_info)
    if user_info:
        pswd = input("Please enter your password: ")
        pswd.rstrip('\n')
        if (user_info[0][1].strip() == pswd):
            print("Successfully logged in as: ", user_info[0][2], "!")
            return (1, int(user_info[0][0]), user_info[0][2])             
        else:
            print("Incorrect username or password, please try again.")
            return (0, None, None)   
    else:
        print("That username does not exist in the system, please try again.")
        return (0, None, None)  
    
  #  type(userID)
  #  type(pswd)
  #  print("UserID:" + userID + "Password:" + pswd + ".")
   # inputarr = [int(userID), pswd.ljust(4)] #password must be padded or it will not match
   # cur.execute("select name from users where usr = :1 and pwd = :2", (int(userID), pswd))

  # name = cur.fetchall()
  #  print(name)
    #name = name[0][0]
  #  if name:
 #       print("Successfully logged in as: ", name, "!")
  #      return (1, int(userID), name) 
  # else:
   #     print("Incorrect username or password, please try again.")
  #      return (0, None, None)
    

# if register is specified prompts the user for all the information to create a user in the table
def register(cur):
    os.system(CLEAR_SCREEN)
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    city = input("Enter the city you live in: ")
    timezone = input("Enter your timezone: ")
    #timezone = float(timezone)
    pswd = input("Enter your password: ")
    # @TODO need to add error checking to all of these to make sure correct information is entered
    #  and maybe a better prompt to specify conditions; maybe use the getValidInput function?

    cur.execute("select NVL(max(usr),-1) from users")
    user = cur.fetchall()
    user = int(user[0][0])
    user = user + 1
    #pdb.set_trace()
    #print("insert into users (usr,pwd,name,email,city,timezone) values (\'"+ str(user) + "\',\'" + pswd + "\',\'" + name +"\',\'" + email + "\',\'" + city + "\',\'" + timezone +"\')")
    cur.execute("insert into users values (:u, :p, :n, :e, :c, :tz)",(user, pswd, name, email, city, timezone))
    print("successfully registered")
    print("Welcome ", name, ", your user ID is ", user, ", don't forget this as it is used to login.")
    print("Thank you for registering with Twitterpated!")
    pause_until_input()
    return 1


def home_page(con, cur, userID):
    os.system(CLEAR_SCREEN)
    '''
    @ TODO this is not complete at all
    Provides the opening homepage for initial user login. It explains
    some controls, and displays tweets of followed users 5 at a time.
    There is an option to go and use the program functions for more
    advanced usage.
    '''
    
    return
    
    print("Welcome to Twitterpated! Here are all your followed users' tweets:")
    # @TODO need to get both tweets and retweets, this query is bad
    cur.execute("select tid, writer, usr, tdate, text, replyto " +
                "from tweets t, users u " +
                "where t1.writer = u1.usr " + 
                "union " + 
                "select tid, writer, usr, rdate, text " + 
                "from retweets r join users u1 on r. users u2, ")


# Provides a menu for the functions of the program
def functions(con, cur, userID):
    os.system(CLEAR_SCREEN)
    print("Welcome to Twitterpated! The functions of Twitterpated are listed below.")

    print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
          "Tweet\n4 - List Followers\n5 - Manage Lists\n6 - Logout")
    f_input = input("What would you like to do? ")

    while f_input:
        if f_input == "1":
            search_tweet(cur)
        elif f_input == "2":
            search_user(cur)
        elif f_input == "3":
            write_tweet(con, cur, userID)
        elif f_input == "4":
            list_followers(cur, userID)
        elif f_input == "5":
            manage_lists(con, cur, userID)
        elif f_input == "6":
            print("Logging out of Twitterpated.")
            return 1
        else:
            print("The input entered was not valid. Please enter one of specified prompts.")

        print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
              "Tweet\n4 - List Followers\n5 - Manage Lists\n6 - Logout")
        f_input = input("What would you like to do? ")

    pause_until_input()
    return 1


# prompts the user to enter a keyword to be searched for in tweets and prints
#  ou the top 5 recent tweets and gives the user the option to select a tweet
#  and get some stats about it or recieve the next 5 tweets.
def search_tweet(cur):
    os.system(CLEAR_SCREEN)
    keyword = input("Please enter the keyword(s) you would like to search. (If you"
                    " are entering more than one keyword, please seperate using"
                    " a ','): ")

    keyword.split(',')
    for word in keyword:
        word = word.strip()
        cur.execute("select text from " + 
                    "(select text, row_number() over (order by tdate desc) as row_num " + 
                    "from tweets where text like ('%' || :word || '%')) where row_num <= 5", (word))
        tweets = cur.fetchall()
        index = 1
        for tweet in tweets:
            print(index, " ", tweet)
            index += 1
        if index > 5:
            more_tweets = input("Would you like to receive the next 5 tweets " + 
                                "with the matching keyword from before? Enter " + 
                                "yes or no: ")
            while (more_tweets == 'yes'):
                cur.execute("select text from " + 
                            "(select text, row_number(order by tdate descending) as row_num " + 
                            "from tweets where text like '%:word%') where row_num <= 5", (word))
                # @TODO not finished
    pause_until_input()
    return

def search_user(cur):
    os.system(CLEAR_SCREEN)
    keyword = input("Please enter the name or city of the user you would like to search for: ")
    keyword = keyword.strip()
    cur.execute(queries.search_users_keyword, [keyword, keyword])
    results = cur.fetchall()
    for row in results:
        print(*row)
        
    #@TODO needs more functions
    pause_until_input()
    return

                
#Gets the user to input a tweet, checks if less than 80 charcters, then adds tweet
# finds where the # are and gets the words, adding them to mentions and then checking
# if it is already in hashtags and if not adding into it.
def write_tweet(con, cur, userID):
    os.system(CLEAR_SCREEN)
    t_text = input("Enter your tweet(Max 80 character): ")
    
    if len(t_text) > 80:
        print("The tweet you have entered is too long, please try again.")
        return
    
    cur.execute("select NVL(max(tid),-1) from tweets")
    tweetID = cur.fetchall()
    tweetID = int(tweetID[0][0])
    tweetID += 1 
    
    print(tweetID)
    
    query = "insert into tweets values (:t, :wrt, SYSDATE, :txt, null)"
    cur.execute(query,{'t':tweetID, 'wrt':userID, 'txt':t_text})
    print("done")
    con.commit()

    
    print ([pos for pos, char in enumerate(t_text) if char == '#'])
    index_hash = ([pos for pos, char in enumerate(t_text) if char == '#'])
    for index in index_hash:
        end_index = index
        while t_text[end_index].isalpha():
            end_index += 1
            
        hash_tag = t_text[index+1:end_index]
        print(hash_tag)
        # might need to check if hashtag is less than 10 characters
                
        query = "insert into mentions values(:t, :ht)"
        cur.execute(query, {'t':tweetID, 'ht':hash_tag})
        
        query = "select * from hashtags where term = :ht"
        cur.execute(query, {'ht',hash_tag})
        trm = cur.fetchall()
        if not trm:
            query = "insert into hashtags value(:h_tag)"
            cur.execute(query, {'h_tag':hash_tag})           
             
    con.commit
    pause_until_input()
    return

def list_followers(cur, userID):
    os.system(CLEAR_SCREEN)
    cur.execute(queries.get_users_followers, [userID])
    followers = cur.fetchall()
    if followers != []:
        for row in followers:
            print(*row)
    else:
        print("You do not seem to have anybody following you... maybe write some tweets?")
    pause_until_input()
    return

def manage_lists(con, cur, userID):
    os.system(CLEAR_SCREEN)
    print("Welcome to list management, what would you like to do?.")
    print("1 - View Your Lists\n2 - See Lists You Are On\n3 - Create a "
          "New List\n4 - Add or Delete Members From Your Lists\n5 - Return to Main Menu")
    f_input = input("What would you like to do? ")

    while f_input:
        if f_input == "1":
            view_user_lists(cur, userID)
        elif f_input == "2":
            view_user_list_membership(cur, userID)
        elif f_input == "3":
            create_list(con, cur, userID)
        elif f_input == "4":
            edit_lists(con, cur, userID)
        elif f_input == "5":
            print("Returning to main menu.")
            return
        else:
            print("The input entered was not valid. Please enter one of specified prompts.")
            
        os.system(CLEAR_SCREEN)
        print("Welcome to list management, what would you like to do?.")
        print("1 - View Your Lists\n2 - See Lists You Are On\n3 - Create a "
          "New List\n4 - Add or Delete Members From Your Lists\n5 - Return to Main Menu")
        f_input = input("What would you like to do? ")
        
    
    pause_until_input()
    return

def view_user_lists(cur, userID):
    os.system(CLEAR_SCREEN)
    cur.execute(queries.get_user_lists, [userID])
    lists = cur.fetchall()
    if lists != []:
        for row in lists:
            print(*row)
    else:
        print("You do not have any lists")
    pause_until_input()
            
def view_user_list_membership(cur, userID):
    os.system(CLEAR_SCREEN)
    cur.execute(queries.get_lists_containing_user, [userID])
    lists = cur.fetchall()
    if lists != []:
        for row in lists:
            print(*row)
    else:
        print("You are not on any lists")
    pause_until_input()

def create_list(con, cur, userID):
    os.system(CLEAR_SCREEN)
    lname = get_valid_input(length = 14, prompt = "What would you like to name your new list (Enter nothing to cancel): ")
    if lname:
        cur.execute(queries.see_if_list_exists, [lname])
        lists = cur.fetchall()
        if lists == []:
            cur.execute(queries.create_new_list, [lname, userID])
            con.commit()
            print("Successfully created list: " + lname)
        else:
            print("Sorry, but that list name has been taken")
        pause_until_input()    
        
def edit_lists(con, cur, userID):
    os.system(CLEAR_SCREEN)
    print("Welcome to list management, what would you like to do?.")
    print("1 - Add to list\n2 - Remove from list\n3 - Return to Main Menu")
    f_input = input("What would you like to do? ")
    while f_input:
        if f_input == "1":
            add_to_list(con, cur, userID)
        elif f_input == "2":
            remove_from_list(cur, userID)
        elif f_input == "3":
            return
        os.system(CLEAR_SCREEN)
        print("Welcome to list management, what would you like to do?.")
        print("1 - Add to list\n2 - Remove from list\n3 - Return to Main Menu")
        f_input = input("What would you like to do? ")
        

def add_to_list(con, cur, userID):
    cur.execute(queries.get_user_lists, [userID])
    lists = cur.fetchall()
    if lists == []:
        print("You do not have any lists. You should go make one!")
        pause_until_input()
        return


    uID = input("Please Enter the user ID you would like to add: ")
    cur.execute(queries.does_user_exist, [uID])
    lists = cur.fetchall()
    if lists != []:
        
        lname = get_valid_input(length = 12, prompt = "Which list would you like to add this user to? (Enter nothing to cancel): ")
        if lname:
            #cur.execute(queries.see_if_list_exists, [lname, uID])
            
            #cur.execute(queries.add_member_to_list, [lname, uID])
            #con.commit()
            #print("Successfully added " + uID + " to list " + lname + ".")
    else:
        print("This user doesn't exist.")
    pause_until_input()
    return

def remove_from_list(cur, userID):
    pause_until_input()
    return

def pause_until_input():
    input("Press Enter To Continue")
