import pdb

def getValidInput(valids, prompt = '', tries = float('inf')):
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
        if instr in valids: break
        print("That is not a valid input")
        attempt = attempt + 1
    if attempt >= tries:
        return None
    return instr


# if login is specified gets the users id and password and checks to see if the user is
#  in the table, returning 1 if they are 0 if they are not
def login(cur):
    userID = input("Please enter your user ID: ")
    pswd = input("Please enter your password: ")

    inputarr = [int(userID), pswd.ljust(4)] #password must be padded or it will not match
    cur.execute("select name from users where usr = :1 and pwd = :2", inputarr)

    name = cur.fetchall()[0][0]
    if name:
        print("Successfully logged in as: ", name, "!")
        return (1, int(userID), name) 
    else:
        print("Incorrect username or password, please try again.")
        return (0, None, None)

# if register is specified prompts the user for all the information to create a user in the table
def register(cur):
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
    return 1

# prompts the user to enter a keyword to be searched for in tweets and prints
#  ou the top 5 recent tweets and gives the user the option to select a tweet
#  and get some stats about it or recieve the next 5 tweets.
def search_tweet(cur):
    keyword = input("Please enter the keyword(s) you would like search. (If you"
                    " are entering more than one keyword, please seperate using"
                    " a ','): ")

    keyword.split(',')
    for word in keyword:
        word.strip()
        cur.execute("select text from " + 
                    "(select text, row_number() over (order by tdate desc) as row_num " + 
                    "from tweets where text like '%:word%') where row_num <= 5", (word)) #@TODO does this correctly execute the %% modifiers? Or is it considering the variable name as "word%"?
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
                #not finished

    return

def search_user(cur):
    return

def write_tweet(cur, login):
    tweet
    return

def list_followers(cur):
    return

def manage_lists(cur):
    return
