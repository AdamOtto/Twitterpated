/*
Needed queries for the project
*/
1.
- Given a keyword, return all tweets that mention the keyword in their text or in their list of hashtags
define @keyword char[20]

select t.text "Text"
from tweets t
where t.text like ('%' || @keyword || '%')


- given a tweet id, return the number of retweets and number of replies.
define @tweetId integer

select (    select count(t.replyto)
            from tweets t
             where t.replyto = @tweetId
        ) replyCount,
        (
            select count(r.tid)
            from retweets r
            where r.tid = @tweetId
        ) retweetCount
from dual


- given a writer id, replyto Id and a text input, insert a reply tweet into tweets.
define @writerId integer, @replyToId integer, @text char[120]
insert into tweets
(tid, writer, tdate, text, replyto)
select (count(*) + 1) "newId", @writerId, CURRENT_DATE, @text,@replyToId
from tweets;


- given a tweet id and a user id, insert a retweet of the tweet id by user id in retweets.
define @tweetId integer, @usrId integer
insert into retweets values (@usrID, @tweetId, CURRENT_DATE);



2.
- given a keyword, return all users whose names contain the keyword followed by the list of cities that contain the key word, sorted from shortest to longest
define @keyword char[20]

select NVL(u1.name, u2.name), NVL(u1.city, u2.city), namelength, citylength
from
  (
    select u1.name, u1.city, rank() over (order by length(replace(u1.name, ' ', '')) asc) as namelength
    from users u1
    where lower(u1.name) like ('%' || @keyword || '%')
  ) u1
  full outer join
  (
    select u2.name, u2.city, rank() over (order by length(replace(u2.city, ' ', '')) asc) as citylength
    from users u2
    where lower(u2.city) like ('%' || @keyword || '%')
  ) u2
  on u1.name = u2.name and u1.city = u2.city
order by namelength, citylength



- given a user id, return the number of tweets they have
define @usrId Integer

select count(*)
from tweets
where writer = @usrId


- given a user id, return the number of users they follow
define @usrId Integer

select count(*)
from follows
where flwer = @usrId

- given a user id, return the number of users following them
define @usrId Integer

select count(*)
from follows
where flwee = @usrId

- given a user id, return their tweets by most recent
define @usrId Integer

select text
from tweets
where writer = @usrId
order by tdate desc



3.
- given a user id and text, insert a tweet with the id and text
define @userId Integer, @text char[120]

insert into tweets
(tid, writer, tdate, text, replyto)
select (count(*) + 1) "newId", @writerId, CURRENT_DATE, @text, null
from tweets;


- given a tid and a hashtag, store an entry into the mentions table
define @tid Integer, @hashtag char[20]

insert into mentions values (@tid, @hashtag);



4.
- given a user id, return all followers of the user
define @usrId Integer

select count(*)
from follows
where flwee = @usrId


- given a user id 'follower' and user id 'followee', insert an entry into the follows table
define @follower Integer, @followee Integer

insert into follows values (@follower, @followee, CURRENT_DATE);


- the same queries for user stats as in 2



5.
- given a user id, return all lists made by the user
define @usrId Integer

select lname
from lists
where owner = @usrId


- given a user id, return all lists that contain the user id
define @usrId Integer

select lname
from includes
where member = @usrId


- given a user id and a list name, insert a new list into the lists table
define @userId Integer, @listName char[20]

insert into lists values (@listName, @userId);


- given a list name, return all users of that list
define @listName char[20]

select u.name
from users u
join includes i on u.usr = i.member
where i.lname = @listName

- given a list name and a user id, remove that user from the list
define @listName char[20], @userId Integer

DELETE FROM includes
where lname = @listName
AND member = @userId;
