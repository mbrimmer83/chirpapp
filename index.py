from flask import Flask, render_template, request, redirect, session

import pg

db = pg.DB(dbname='chirpdb')

app = Flask('ChirpApp')

@app.route('/')
def home():
    return render_template(
    'home.html'
    )


@app.route('/profile')
def profile():
    query1 = db.query('''select * from users where users.id = $1''',1)
    query2 = db.query('''select count(tweets.tweetid) from tweets inner join users on tweets.user_id = users.id where users.id = $1''',1)
    query3 = db.query('''select count(follow.id) from follow where follow.followee = $1''',1)
    query4 = db.query('''select count(follow.id) from follow where follow.follower = $1''',1)
    query5 = db.query('''select * from tweets where tweets.user_id = $1 order by tweet_date_time''',1)
    print query5.namedresult()[0].tweet_date_time
    return render_template(
        'profile.html',
        user = query1.namedresult()[0],
        tweets = query2.namedresult()[0],
        followee = query3.namedresult()[0],
        follower = query4.namedresult()[0],
        tweetcontent = query5.namedresult()
    )

@app.route('/timeline')
def timeline():
    query1 = db.query('''select * from users where users.id = $1''',1)
    query2 = db.query('''select count(tweets.tweetid) from tweets inner join users on tweets.user_id = users.id where users.id = $1''',1)
    query3 = db.query('''select count(follow.id) from follow where follow.followee = $1''',1)
    query4 = db.query('''select count(follow.id) from follow where follow.follower = $1''',1)
    query5 = db.query('''select
    	timeline.tweet_content, timeline.tweet_date_time, users.username, timeline.likes, timeline.retweet_num
    from
    (select
      	tweets.tweet_content, tweets.tweet_date_time, tweets.user_id, tweets.likes, tweets.retweet_num
    from
    	tweets
    inner join
      	follow on tweets.user_id = follow.followee
    where
    	follow.follower = $1
    union
    select
        tweets.tweet_content, tweets.tweet_date_time, tweets.user_id, tweets.likes, tweets.retweet_num
    from
      	tweets
    where
     	tweets.user_id = $1) as timeline
    inner join
    	users on timeline.user_id = users.id
    order by
    	tweet_date_time
''',1)
    print query5.namedresult()
    return render_template(
        'timeline.html',
        user = query1.namedresult()[0],
        tweets = query2.namedresult()[0],
        followee = query3.namedresult()[0],
        follower = query4.namedresult()[0],
        timeline_tweets = query5.namedresult()
    )
@app.route('/signup')
def signup():
    return render_template(
    'signup.html'
    )

@app.route('/sign_up')
def sign_up():
    return render_template(
    'home.html'
    )

@app.route('/login')
def login():
    print 'login'

@app.route('/follow')
def follow():
    print 'follow'

@app.route('/like')
def like():
    print 'Like'

@app.route('/retweet')
def retweet():
    print 'Retweet'

if __name__ == '__main__':
    app.debug = True
    app.run(debug = True)
