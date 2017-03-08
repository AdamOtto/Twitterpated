--users(usr,pwd, name,email,city,timezone)
insert into users values (1,'passw0rd','Don Iveson','di@doniveson.ca','Edmonton',-7);
insert into users values (2,'passw0rd','Jim Wu','djjim@gmail.com','Calgary',-7);
insert into users values (3,'passw0rd','George Bush','gbush@twtr.com','Washington',-5);
insert into users values (4,'passw0rd','Derrick Wai','dwai@uab.ca','Edmonton',-7);
insert into users values (5,'passw0rd','Taylor Swift','tswift@twtr.com','Nashville',-6);
insert into users values (6,'passw0rd','Joffrey Lupul','jlu@nhl.com','Toronto',-5);
insert into users values (7,'passw0rd','Nicolas Cage','ncage@twtr.com','Sacramento',-7);

--follows(flwer,flwee,start_date)
insert into follows values (2,1,'01-SEP-2015');
insert into follows values (3,1,'26-AUG-2016');
insert into follows values (6,1,'28-AUG-2015');
insert into follows values (7,1,'05-JUN-2014');
insert into follows values (1,2,'17-SEP-2016');
insert into follows values (1,7,'19-SEP-2015');

--tweets(tid,writer,tdate,text,replyto)
insert into tweets values (1,2,'05-SEP-2014','hey girl, feel my sweater, know what it''s made of? boyfriend material',null);
insert into tweets values (2,3,'25-JAN-2017','Thats not what sweaters are made of.',1);
insert into tweets values (3,7,'04-AUG-2016','This is a tweet with text in it.',1);
insert into tweets values (4,1,'06-JUN-2016','My apologies #edmonton, the Metro line has been delayed to 2018',null);
insert into tweets values (5,6,'25-JUL-2016','First tweet! Hello world! Hello #Edmonton!',null);
insert into tweets values (6,5,'25-JUL-2016','bout to drop the hottest mixtape of 2064!!!!',5);
insert into tweets values (7,7,'02-JUN-1989','IM A VAMPIRE! IM A VAMPIRE! IM A VAMPIRE!',null);

--hashtags(term)
insert into hashtags values ('edmonton');

--mentions(tid,term)
insert into mentions values (4, 'edmonton');
insert into mentions values (5, 'edmonton');

--retweets(usr,tid,rdate)
insert into retweets values (2,1,'12-JAN-2017');
insert into retweets values (3,1,'25-APR-2015');
insert into retweets values (4,1,'08-SEP-2014');
insert into retweets values (5,6,'03-DEC-2016');

--lists(lname,owner)
insert into lists values ('canadian', 3);

--includes(lname,member)
insert into includes values ('canadian', 1);
insert into includes values ('canadian', 4);
insert into includes values ('canadian', 7);

