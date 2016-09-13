CREATE TABLE users (
  id serial PRIMARY KEY,
  name varchar,
  email varchar,
  username varchar,
  password varchar,
  pic_id integer
);

CREATE TABLE tweets (
  tweetid serial PRIMARY KEY,
  user_id integer REFERENCES users (id),
  tweet_date_time timestamp default current_timestamp,
  tweet_content varchar (141),
  likes integer,
  retweet_num integer,
  retweet_user_name varchar
);

insert into tweets values(default, 1, default, 'Hello World', 0, 0, FALSE, null);

CREATE TABLE retweet (
  retweetid serial PRIMARY KEY,
  tweet_id integer REFERENCES tweets (tweetid),
  retweet_date_time timestamp default current_timestamp,
  user_id integer REFERENCES users (id)
);

CREATE TABLE follow (
  id serial PRIMARY KEY,
  follower integer REFERENCES users (id),
  followee integer REFERENCES users (id)
);

select
  *
from
  tweets
inner join
  follow on follow.followee = tweets.user_id
inner join
  retweet on retweet.tweetid = tweets.id and follow.followee = retweet.user_id
where
  follow.follower = ME


  select
  	*
  from
  	tweets
  inner join
  	follow on tweets.user_id = follow.followee
  where
  	tweets.user_id = 1

    select
    	tweets.tweet_content, users.username, tweets.tweet_date_time, tweets.likes,
    	tweets.retweets
  from
  	tweets
  inner join
    	follow on tweets.user_id = follow.followee
  left outer join
  	users on users.id = tweets.user_id
  order by
  	tweet_date_time
