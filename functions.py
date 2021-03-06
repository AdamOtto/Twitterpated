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
        print("Sorry you have failed to enter valid input too many times, please try again later")
        return None
    return instr


# if login is specified gets the users id and password and checks to see if the user is
#  in the table, returning 1 if they are 0 if they are not
def login(cur):
    userID = input("Please enter your user ID (Enter nothing to return to menu): ").strip()
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
    
    if user_info:
        pswd = input("Please enter your password: ")
        pswd.rstrip('\n')
        if (user_info[0][1].strip() == pswd):
            print("Successfully logged in as: ", user_info[0][2], "!")
            return (1, int(user_info[0][0]), user_info[0][2].strip())             
        else:
            print("Incorrect username or password, please try again.")
            return (0, None, None)   
    else:
        print("That username does not exist in the system, please try again.")
        return (0, None, None)  
    

# if register is specified prompts the user for all the information to create a user in the table
def register(cur):
    clear_screen()
    name = get_valid_input(prompt = "Enter your name (Max 20 chars): ", length = 20, tries = 5)
    if name is None:
        print("Registration Failure, returning to menu")
        pause_until_input()
        return 0
    
    email = get_valid_input(prompt = "Enter your email (Max 15 chars): ", length = 15, tries = 5)
    if email is None:
        print("Registration Failure, returning to menu")
        pause_until_input()
        return 0
    
    city = get_valid_input(prompt = "Enter the city you live in (Max 12 chars): ", length = 12, tries = 5)
    if city is None:
        print("Registration Failure, returning to menu")
        pause_until_input()
        return 0
 
    timezone = get_valid_input(prompt = "Enter your timezone (Float or Int): ", length = 10, tries = 5)
    try:
        timezone = float(timezone)
    except:
        pass
    if timezone is None:
        print("Registration Failure, returning to menu")
        pause_until_input()
        return 0
    elif not isinstance(timezone, (float)):
        print("Timezone must be a number (float or int), Registration failure, returning to menu")
        pause_until_input()
        return 0

    pswd = get_valid_input(prompt = "Enter your password (Max 4 chars): ", length = 4, tries = 5)
    if pswd is None:
        print("Registration Failure, returning to menu")
        pause_until_input()
        return 0


    cur.execute("select NVL(max(usr),-1) from users")
    user = cur.fetchall()
    user = int(user[0][0])
    user = user + 1
    cur.execute("insert into users values (:u, :p, :n, :e, :c, :tz)",(user, pswd, name, email, city, timezone))
    print("successfully registered")
    print("Welcome ", name, ", your user ID is ", user, ", don't forget this as it is used to login.")
    print("Thank you for registering with Twitterpated!")
    pause_until_input()
    return 1


def home_page(con, cur, userID, username):
    clear_screen()
    '''
    Provides the opening homepage for initial user login. It explains
    some controls, and displays tweets of followed users 5 at a time.
    There is an option to go and use the program functions for more
    advanced usage.
    '''
    
    print("Welcome to Twitterpated " + username +"! Here are all your followed users' tweets:")
            
    cur.execute(queries.show_followed_users_activity, {'ID':userID})
    
    end = False
    skip_print = False
    print("ID:".ljust(3) + " " + "User:".ljust(20) + " " + "Action:".ljust(7) + " " + "Tweet Text:".ljust(80))
    while True:
        if not skip_print:
            results = cur.fetchmany(numRows = 5)
            for row in results:
                print(str(row[0]).ljust(3) + " " + row[4].ljust(20) + " " + ("retweet".rjust(7) if row[3]==1 else "tweet".rjust(7)) + " " + str(row[1]))
                
        # this skip_print is for if you get an error in inputs later and need to continue the loop without advancing.
        skip_print = False 
        if len(results) != 5: #this is the end of the list, menu options need to change
            print("There are no more results.")
            choice = input("[Tweet ID#] = view tweet stats, anything else goes to functions menu: ")
            end = True
            
        if not end: choice = blanking_input("[Enter] = see more, [Tweet ID#] = view tweet stats, anything else goes to functions menu: ") #regular menu options
        if choice == "" and not end:
            continue
        try:
            choice = int(choice)
        except:
            print("A tweet ID must be a number")
        if type(choice) == int:
            cur2 = con.cursor()
            cur2.execute("select * from tweets where tid = :id", [choice])
            check_user_results = cur2.fetchone()
            if check_user_results is None:
                blanking_input("Sorry, but that tweet does not exist, enter to continue") #make a dissapearing error prompt
                skip_print = True #We need to continue the loop, but not move the cursor
                continue
            view_tweet(con, cur, userID, choice)
            return
        print("Search ended")
        break


# Provides a menu for the functions of the program
def functions(con, cur, userID, username):
    clear_screen()
    print("The functions of Twitterpated are listed below.")

    print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
          "Tweet\n4 - List Followers\n5 - Manage Lists\n6 - Logout")
    f_input = input("What would you like to do? ")

    while f_input:
        if f_input == "1":
            search_tweet(con, cur, userID)
        elif f_input == "2":
            search_user(con, cur, userID)
        elif f_input == "3":
            write_tweet(con, cur, userID, None)
        elif f_input == "4":
            list_followers(con, cur, userID)
        elif f_input == "5":
            manage_lists(con, cur, userID)
        elif f_input == "6":
            print("Logging out of Twitterpated.")
            return 1
        else:
            print("The input entered was not valid. Please enter one of specified prompts.")
            
        clear_screen()
        print("1 - Search for Tweets\n2 - Search for Users\n3 - Write a "
              "Tweet\n4 - List Followers\n5 - Manage Lists\n6 - Logout")
        f_input = input("What would you like to do? ")

    pause_until_input()
    return 1


# prompts the user to enter a keyword to be searched for in tweets and prints
#  out the top 5 recent tweets and gives the user the option to select a tweet
#  and get some stats about it or recieve the next 5 tweets.
def search_tweet(con, cur, userID):
    clear_screen()
    keyword = input("Please enter the keyword(s) you would like to search. (If you"
                    " are entering more than one keyword, please seperate using"
                    " a ','): ")
    keyword = keyword.split(',')
    #Algorithmically build a query that searches for keywords and hashtags
    key_str = ""
    hash_str = ""
    key_list = []
    hash_list = []
    i = 0
    for word in keyword:
        word = word.strip()
        i = i+1
        if word[:1] != '#': #this method safely handles empty keywords
            #keyword
            if key_str == "": #first entry
                key_str = key_str + "LOWER(t.text) like ('%' || LOWER(:" + str(i) + ") || '%')"
            else:
                key_str = key_str + " or LOWER(t.text) like ('%' || LOWER(:" + str(i) + ") || '%')"
            key_list.append(word.lower())
        else:
            #hashtag
            if hash_str == "": #first entry
                hash_str = hash_str + "LOWER(replace(m.term, ' ', '')) = :" + str(i)
            else:
                hash_str = hash_str + " or LOWER(replace(m.term, ' ', '')) = :" + str(i)
            hash_list.append(word[1:].lower()) #adds the word without the hash symbol
    #now that the strings are built, build the total query and list of variables
    terms_list = key_list + hash_list
        
    #this query uses distinct, because multiple hashtags in a tweet create duplicate entries, tid stops 
    #this from clearing out retweets
    query = """
    select distinct t.tid, extract(month from t.tdate) as month, extract(day from t.tdate) as day, extract(year from t.tdate) as year, u.name, t.text, t.tdate
    from tweets t, mentions m, users u
    where t.writer = u.usr"""
    
    #Add the conditions based on if they need to exist or not
    if key_str == "":
        if hash_str == "":
            pass
        else:
            query = query + " and m.tid = t.tid and (" + hash_str + ")"
    else:
        if hash_str == "":
            query = query + " and (" + key_str + ")"
        else:
            query = query + " and ((" + key_str + ") or ((" + hash_str + ") and m.tid = t.tid)"
    
    query = query + " order by t.tdate desc"
    
    cur.execute(query, terms_list)
    
    #This Handles 5 at a time showing
    end = False
    skip_print = False
    print("Tweet ID:\t Name:" + ' '*15 + "Tweet Text:")
    while True:
        if not skip_print:
            results = cur.fetchmany(numRows = 5)
            for row in results:
                  print(str(row[0]).ljust(3) + "\t\t " + str(row[4]) + ' '*(20-len(str(row[4]))) + str(row[5]))

        # this skip_print is for if you get an error in inputs later and need to continue the loop without advancing.
        skip_print = False 
        if len(results) != 5: #this is the end of the list, menu options need to change
            print("There are no more results.")
            choice = input("[Tweet ID#] = view tweet stats, anything else cancels: ")
            end = True
        if not end: choice = blanking_input("[Enter] = see more, [Tweet ID#] = view tweet stats, anything else cancels: ") #regular menu options
        if choice == "" and not end:
            continue
        try:
            choice = int(choice)
        except:
            print("A tweet ID must be a number")
        if type(choice) == int:
            cur2 = con.cursor()
            cur2.execute("select * from tweets where tid = :id", [choice])
            check_user_results = cur2.fetchone()
            if check_user_results is None:
                blanking_input("Sorry, but that tweet does not exist, enter to continue") #make a dissapearing error prompt
                skip_print = True #We need to continue the loop, but not move the cursor
                continue
            view_tweet(con, cur, userID, choice)
            return
        print("Search ended")
        break

    pause_until_input()
    return


# Finds users or cities that match the keyword displays them 5 at a time, prompting a user if they
#  want to see more or look at a specific user stats and tweets, with the ability to follow them.
def search_user(con, cur, userID):
    clear_screen()
    keyword = input("Please enter the name or city of the user you would like to search for: ")
    keyword = keyword.strip()
    cur.execute(queries.search_users_keyword, [keyword, keyword])
    #This Handles 5 at a time showing
    end = False
    skip_print = False
    
    print("User ID:\t Name:" + ' '*15 + "City:")
    while True:
        if not skip_print:
            results = cur.fetchmany(numRows = 5)
            for row in results:
                print(str(row[0]) + "\t\t " + str(row[1]) + ' '*(20-len(str(row[1]))) + str(row[2]))
        
        # this skip_print is for if you get an error in inputs later and need to continue the loop without advancing.
        skip_print = False 
        if len(results) != 5: #this is the end of the list, menu options need to change
            print("There are no more results.")
            choice = input("[ID#] = view user, anything else cancels: ")
            end = True
        if not end: choice = blanking_input("[Enter] = see more, [ID#] = view user, anything else cancels: ") #regular menu options
        if choice == "" and not end:
            continue
        try:
            choice = int(choice)
        except:
            print("Not a valid user ID")
        if type(choice) == int:
            cur2 = con.cursor()
            cur2.execute("select * from users where usr = :id", [choice])
            check_user_results = cur2.fetchone()
            if check_user_results is None:
                blanking_input("Sorry, but that user does not exist, enter to continue") #make a dissapearing error prompt
                skip_print = True #We need to continue the loop, but not move the cursor
                continue
            view_user(con, cur, userID, choice)
            return
        print("Search ended")
        break
        
    pause_until_input()
    return

                
#Gets the user to input a tweet, checks if less than 80 charcters, then adds tweet
# finds where the # are and gets the words, adding them to mentions and then checking
# if it is already in hashtags and if not adding into it.
def write_tweet(con, cur, userID, reply):
    clear_screen()
    t_text = input("Enter your tweet(Max 80 character): ")
    
    if len(t_text) > 80:
        print("The tweet you have entered is too long, please try again.")
        return
    
    cur.execute("select NVL(max(tid),-1) from tweets")
    tweetID = cur.fetchall()
    tweetID = int(tweetID[0][0])
    tweetID += 1 
   
    query = "insert into tweets values (:t, :wrt, SYSDATE, :txt, :rep)"
    cur.execute(query,{'t':tweetID, 'wrt':userID, 'txt':t_text, 'rep':reply})
    con.commit()

    #gets positions of the '#' in the text.
    index_hash = ([pos for pos, char in enumerate(t_text) if char == '#'])
    
    for index in index_hash:
        end_index = index + 1
        while t_text[end_index].isalpha():
            end_index += 1
            if end_index >= len(t_text):
                break
        
        #gets the hash_tag from the original tweet based on the index's
        hash_tag = t_text[index+1:end_index]
        
        if len(hash_tag) <= 10 and len(hash_tag) > 0:
            cur.execute("select * from hashtags where term = '" + hash_tag + "'")
            trm = cur.fetchone()
            
            if not trm:
                query = "insert into hashtags values (:h_tag)"
                cur.execute(query, {'h_tag':hash_tag})  
                con.commit()
                    
            query = "insert into mentions values (:t, :ht)"
            cur.execute(query, {'t':tweetID, 'ht':hash_tag}) 
            con.commit()
        
        else:
            print("The hashtag from the tweet was too long to be entered,"
                  "but the tweet was inserted.")
                 
    pause_until_input()
    return

def list_followers(con, cur, userID):
    clear_screen()
    cur.execute(queries.get_users_followers, [userID])
    followers = cur.fetchall()
    if followers != []:
        print("User ID:\t Name:")
        for row in followers:
            print(str(row[0]) + "\t\t " + str(row[1]))
            
        Search = True
        while(Search):
            uID = input("Enter a users ID to see more (leave blank to exit): ")
            if(uID == ''):
                break
            for row in followers:
                if( uID == str(row[0]) ):
                    list_followers_see_more_information(con, cur, userID, uID)
                    Search = False
                    break
    else:
        print("You do not seem to have anybody following you... maybe write some tweets?")
    pause_until_input()
    return

# Gets more information about a user
def list_followers_see_more_information(con, cur, userID, uID):
    clear_screen()
    #Get the data of the selected user.
    cur.execute(queries.get_following_users_data, [uID])
    follower_tweet_count = cur.fetchall()
    print("This user has written " + str(follower_tweet_count[0][0]) + " tweets.")
    print("This user is following " + str(follower_tweet_count[0][1]) + " user(s).")
    print("This user has " + str(follower_tweet_count[0][2]) + " follower(s).\n")
    view_user(con, cur, userID, uID)
    return


# Creates a menu for lists where a user can choose to view their lists, see lists they are in
#  create a list, edit a list, or return.
def manage_lists(con, cur, userID):
    clear_screen()
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
            
        clear_screen()
        print("Welcome to list management, what would you like to do?.")
        print("1 - View Your Lists\n2 - See Lists You Are On\n3 - Create a "
          "New List\n4 - Add or Delete Members From Your Lists\n5 - Return to Main Menu")
        f_input = input("What would you like to do? ")
        
    
    pause_until_input()
    return


# Views the lists that the user has created
def view_user_lists(cur, userID):
    clear_screen()
    cur.execute(queries.get_user_lists, [userID])
    lists = cur.fetchall()
    if lists != []:
        for row in lists:
            print(*row)
    else:
        print("You do not have any lists")
    pause_until_input()
    
    
# View the list that the user is a part of            
def view_user_list_membership(cur, userID):
    clear_screen()
    cur.execute(queries.get_lists_containing_user, [userID])
    lists = cur.fetchall()
    if lists != []:
        for row in lists:
            print(*row)
    else:
        print("You are not on any lists")
    pause_until_input()

    
# create a new list for the user
def create_list(con, cur, userID):
    clear_screen()
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
        
        
# If editing a list was selected, brings up this menu where a user can specify
#  if they want to add or remove someone from a list or return to previous menu       
def edit_lists(con, cur, userID):
    clear_screen()
    print("Welcome to list management, what would you like to do?.")
    print("1 - Add to list\n2 - Remove from list\n3 - Return to Main Menu")
    f_input = input("What would you like to do? ")
    while f_input:
        if f_input == "1":
            add_to_list(con, cur, userID)
        elif f_input == "2":
            remove_from_list(con, cur, userID)
        elif f_input == "3":
            return
        clear_screen()
        print("Welcome to list management, what would you like to do?.")
        print("1 - Add to list\n2 - Remove from list\n3 - Return to Main Menu")
        f_input = input("What would you like to do? ")
        

# adds a user to a list
def add_to_list(con, cur, userID):
    cur.execute(queries.get_user_lists, [userID])
    lists = cur.fetchall()
    if lists == []:
        print("You do not have any lists. You should go make one!")
        pause_until_input()
        return

    uID = input("Please Enter the user ID you would like to add: ")
    #Test if the user exists
    cur.execute(queries.does_user_exist, [uID])
    lists = cur.fetchall()
    if lists != []:        
        lname = get_valid_input(length = 12, prompt = "Which list would you like to add this user to? (Enter nothing to cancel): ")
        if lname:
            #Test if the list exists and belongs to user.
            cur.execute("select * from lists where lname = '" + lname +  "' AND owner = " + str(userID))
            lists = cur.fetchall()
            
            if lists != []:
                #Test if the user is already in the list.
                cur.execute("select * from includes where lname = '" + lname +  "' AND member = " + str(uID))
                lists = cur.fetchall()
                
                if lists == []:
                    #Update the list with the new user.
                    cur.execute("insert into includes values ('" + lname + "', " + str(uID) + ")")
                    con.commit()
                    print("Successfully added " + uID + " to list " + lname + ".")
                    
                else:
                    print("This user is already in this list!!!");
                    
            else:
                print("This list doesn't exist. Did you misstype it?")
                
    else:
        print("This user doesn't exist.")
    
    pause_until_input()
    return


# removes a user from a list
def remove_from_list(con, cur, userID):
    cur.execute(queries.get_user_lists, [userID])
    lists = cur.fetchall()
    if lists == []:
        print("You do not have any lists. You should go make one!")
        pause_until_input()
        return

    lname = get_valid_input(length = 12, prompt = "Which list would you like to remove from? (Enter nothing to cancel): ")
    if lname:
        #Test if list exists and belongs to user
        cur.execute("select * from lists where lname = '" + lname +  "' AND owner = " + str(userID))
        lists = cur.fetchall()
        
        if lists != []:
            uID = input("Please Enter the user ID you would like to remove: ")
            #Test if the user exists in the list
            cur.execute("select * from includes where lname = '" + lname +  "' AND member = " + str(uID))
            lists = cur.fetchall()
            
            if lists != []:
                 #Remove the user from the list
                 cur.execute("DELETE FROM includes where lname = '" + lname + "' AND member = " + str(uID))
                 con.commit()
                 print("Successfully removed " + uID + " from list " + lname + ".")
                
            else:
                print("This user is not in this list") 
                
        else:
            print("This list doesn't exist. Did you misstype it?")
            
    pause_until_input()
    return


def pause_until_input():
    input("Press Enter To Continue")
   

def blanking_input(prompt):
    '''
    Gets input using the specified prompt, then deletes the prompt
    '''
    instr = input(prompt)
    print("\033[F", end = '') #clear away the input, this returns to previous line
    print((len(prompt) + len(instr))*" ", end = '\r') #write over prompt with spaces, then return to start of line
    return instr


def view_user(con, cur, userID, viewID):
    '''
    shows user stats and tweets for user viewID, option for userID to follow viewID is presented
    '''
    #Show stats
    clear_screen()
    cur.execute(queries.get_user_name, [viewID])
    name = cur.fetchone()
    name = name[0].strip()
    print("Stats about " + name)
    cur.execute(queries.get_user_tweet_count, [viewID])
    twt_cnt = cur.fetchone()
    twt_cnt = twt_cnt[0]
    print("Number of tweets: " + str(twt_cnt))
    cur.execute(queries.get_user_follows_count, [viewID])
    flw_cnt = cur.fetchone()
    flw_cnt = flw_cnt[0]
    print("Number of people they follow: " + str(flw_cnt))
    cur.execute(queries.get_user_follower_count, [viewID])
    flwe_cnt = cur.fetchone()
    flwe_cnt = flwe_cnt[0]
    print("Number of people who follow them: " + str(flwe_cnt))
    cur.execute(queries.get_user_tweets, [viewID])
    
    #Show tweets, first 3 at a time and then 5 at a time
    print("\nHere are " + name + "'s most recent tweets:")
    first_time = True
    end = False
    while True:
        results = cur.fetchmany(numRows = 3 if first_time else 5)
        
        for row in results:
            print(*row)
        
        if len(results) == 0 and first_time:
            print("This user has no tweets.")
            end = True
            
        if (len(results) < 5 and not first_time) or (first_time and len(results) < 3):
            print("This user has no more tweets.")
            end = True
        first_time = False
        if not end:
            choice = blanking_input("[Enter] = more tweets, [f] = follow them, everything else = return: ")
        else:
            choice = blanking_input("[f] = follow them, everything else = return: ")
            
        if choice == "" and not end:
            continue
        elif choice =="f":
            cur2 = con.cursor()
            cur2.execute("select * from follows where flwer = :userID and flwee = :viewID", [userID, viewID])
            check = cur2.fetchone()
            if check is None or check == []:
                cur2.execute(queries.create_flw_follower_follows_followee, [userID, viewID])
                con.commit()
                blanking_input("You have successfully begun following " + name)
            else:
                blanking_input("You already follow " + name + "!") 
        else:
            print("Finished viewing")
            return
    #this is a catch all in case something goes wrong (usually it will return without pausing)        
    pause_until_input()
    return
    
    
def view_tweet(con, cur, userID, tid):
    '''
    Shows stats about a selected tweet with tweet id tid. The option to reply to or retweet the tweet that is viewed
    '''
    clear_screen()
    print("You are looking at the tweet with id # " + str(tid))
    cur.execute("select t.tdate, u.name, t.text from users u, tweets t where t.writer = u.usr and t.tid = :id", [tid])
    stats = cur.fetchone()
    print("\n\"" + stats[2].strip() + "\"\n")
    print("This tweet was written by: " + stats[1].strip())
    print("It was written on: " + str(stats[0]).strip())
    
    #get retweet count
    cur.execute(queries.get_tweet_rtwts, [tid])
    retweets = cur.fetchone()
    retweets = retweets[0]
    print("This tweet has been retweeted this many times: " + str(retweets))
    
    #get reply count
    cur.execute(queries.get_tweet_reps, [tid])
    replies = cur.fetchone()
    replies = replies[0]
    print("This tweet has been replied to this many times: " + str(replies))
    print("")
    choice = get_valid_input(prompt = "1 = reply to this tweet, 2 = retweet this tweet, anything else = exit: ")
    
    if choice == '1':
        print("You will now be taken to a screen where you can write a reply to this tweet")
        pause_until_input()
        write_tweet(con, cur, userID, tid)
        return
    elif choice == '2':
        retweet(con, cur, userID, tid)
    
    pause_until_input()
    return
        
    
# Makes a retweet for the user
def retweet(con, cur, userID, tweetID):
    '''
    Retweets the tweet with tweet id tid under the user with user id userID.
    '''
    query = "select * from retweets r where r.usr = :usrID and r.tid = :twtID"
    cur.execute(query, {'usrID':userID, 'twtID':tweetID})
    check = cur.fetchone()
    
    # check if check is empty, if so make retweet
    if not check:
        cur.execute(queries.create_retweet, [userID, tweetID])
        con.commit()
        print("You have reweeted this tweet successfully")
    else:
        print("I'm sorry, but you have already retweeted this tweet before")
    return

def clear_screen():
    os.system(CLEAR_SCREEN)
