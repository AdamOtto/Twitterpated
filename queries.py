########################HOMEPAGE######################
'''
Given a user id, return all the tweets and retweets of all the users followers, sorted by date.
'''
show_followed_users_activity = """
select t.tid, t.text, t.tdate
from tweets t, follows f
where f.flwer = :ID and f.flwee = t.writer
union
select t.tid, t.text, r.rdate
from retweets r, follows f, tweets t
where f.flwer = :ID and f.flwee = r.usr and t.tid = r.tid
order by tdate desc
"""

########################Question 1####################
'''
Given a keyword, return all tweets that mention the keyword in their text or in their list of hashtags
define @keyword char[20]
'''
#This query needed to be built algorithmically, please see the code in functions.search_tweet()

'''
given a tweet id, return the number of retweets and number of replies.
define @tweetId integer
'''

get_tweet_rtwts_reps = '''
select (    select count(t.replyto)
            from tweets t
             where t.replyto = :tweetId
        ) replyCount,
        (
            select count(r.tid)
            from retweets r
            where r.tid = :tweetId
        ) retweetCount
from dual
'''
get_tweet_reps = '''
select count(t.replyto)
from tweets t
where t.replyto = :tweetId
'''
get_tweet_rtwts = '''
select count(r.tid)
from retweets r
where r.tid = :tweetId
'''

'''
given a writer id, replyto Id and a text input, insert a reply tweet into tweets.
define @writerId integer, @replyToId integer, @text char[120]
'''

create_reply_tweet = '''
insert into tweets
(tid, writer, tdate, text, replyto)
select (count(*) + 1) "newId", :writerId, CURRENT_DATE, :text,:replyToId
from tweets
'''

'''
given a tweet id and a user id, insert a retweet of the tweet id by user id in retweets.
define @tweetId integer, @usrId integer
'''

create_retweet = '''
insert into retweets values (:usrID, :tweetId, CURRENT_DATE)
'''


########################Question 2####################
'''
given a keyword, return all users whose names contain the keyword followed by the list of cities that contain the key word, sorted from shortest to longest
define @keyword char[20]
'''
# @TODO remove namelength, citylength for production
search_users_keyword = """
	select NVL(u1.usr, u2.usr), NVL(u1.name, u2.name), NVL(u1.city, u2.city)
	from
	(
	select u1.usr, u1.name, u1.city, rank() over (order by length(replace(u1.name, ' ', '')) asc) as namelength
	from users u1
	where lower(u1.name) like ('%' || lower(:keyword) || '%')
	) u1
	full outer join
	(
	select u2.usr, u2.name, u2.city, rank() over (order by length(replace(u2.city, ' ', '')) asc) as citylength
	from users u2
	where lower(u2.city) like ('%' || lower(:keyword) || '%')
	) u2
	on u1.name = u2.name and u1.city = u2.city
	order by namelength, citylength
	"""



'''
given a user id, return the number of tweets they have
define @usrId Integer
'''
get_user_tweet_count = '''
select count(*)
from tweets
where writer = :usrId
'''

'''
given a user id, return the number of users they follow
define @usrId Integer
'''
get_user_follows_count = '''
select count(*)
from follows
where flwer = :usrId
'''

'''
given a user id, return the number of users following them
define @usrId Integer
'''
get_user_follower_count = '''
select count(*)
from follows
where flwee = :usrId
'''

'''
given a user id, return their tweets by most recent
define @usrId Integer
'''

get_user_tweets = '''
select text
from tweets
where writer = :usrId
order by tdate desc
'''

'''
given a user id, return the user name
'''
get_user_name = '''
select name
from users u
where u.usr = :usrID
'''

'''
given a user id 'follower' and user id 'followee', insert an entry into the follows table
define @follower Integer, @followee Integer
'''
create_flw_follower_follows_followee = '''
insert into follows values (:follower, :followee, CURRENT_DATE)
'''

########################Question 3####################
'''
given a user id and text, insert a tweet with the id and text
define @userId Integer, @text char[120]
'''
create_tweet = '''
insert into tweets
(tid, writer, tdate, text, replyto)
select (count(*) + 1) "newId", :writerId, CURRENT_DATE, :text, null
from tweets
'''

'''
given a tid and a hashtag, store an entry into the mentions table
define @tid Integer, @hashtag char[20]
'''

create_mention_by_hashtag = '''
insert into mentions values (:tid, :hashtag)
'''


########################Question 4####################
'''
given a user id, return all followers of the user
define @usrId Integer
'''
get_users_followers = '''
select usr, name
from follows, users
where flwee = :usrId and flwer = usr
'''

get_following_users_data = '''
select *
from 
(
select count(*)"tweets Count" from tweets where writer = :usrId
),
(
select count(*)"Following Count" from follows where flwer = :usrId
),
(
select count(*)"Followers Count" from follows where flwee = :usrId
)
'''

'''
the same queries for user stats as in 2
'''


########################Question 5####################
'''
given a user id, return all lists made by the user
define @usrId Integer
'''
get_user_lists = '''
select lname
from lists
where owner = :usrId
'''

'''
given a user id, return all lists that contain the user id
define @usrId Integer
'''
get_lists_containing_user = '''
select lname
from includes
where member = :usrId
'''

'''
given a string, see if there is a list with that exact name
'''
see_if_list_exists = '''
select *
from lists
where lists.lname = :testname
'''

'''
given a user id and a list name, insert a new list into the lists table
define @userId Integer, @listName char[20]
'''
create_new_list = '''
insert into lists values (:listName, :userId)
'''

'''
given a list name, return all users of that list
define @listName char[20]
'''
get_list_members = '''
select u.name
from users u
join includes i on u.usr = i.member
where i.lname = :listName
'''

'''
given a list name and a user id, remove that user from the list
define @listName char[20], @userId Integer
'''
delete_member_from_list = '''
DELETE FROM includes
where lname = :listName
AND member = :userId;
'''

'''
Check to see if a user exists.  We don't want someone to add
a user that doesn't exist to their lists.
define @userId Integer
'''
does_user_exist = '''
select u.usr
from users u
where u.usr = :userId
'''

'''
Determine if a list belongs to a user.  We don't want one
user editing the list of another.
'''
check_if_list_belongs_to_user = '''
select *
from lists
where lname = :listName
AND owner = :userId
'''

'''
Adds a new user to a list
define @listName char[12], @userId Integer
'''
add_member_to_list = '''
insert into includes values (:listName, :userId);
'''
