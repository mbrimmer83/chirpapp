from flask import Flask, render_template, request, redirect, session

import pg
import bcrypt

db = pg.DB(dbname='chirpdb')

app = Flask('ChirpApp')

@app.route('/')
def home():
    return render_template(
    'home.html'
    )


@app.route('/profile')
def profile():
    if 'id' in session:
        query1 = db.query('''select * from users where users.id = $1''',session['id'])
        query2 = db.query('''select count(tweets.tweetid) from tweets inner join users on tweets.user_id = users.id where users.id = $1''',1)
        query3 = db.query('''select count(follow.id) from follow where follow.followee = $1''',session['id'])
        query4 = db.query('''select count(follow.id) from follow where follow.follower = $1''',session['id'])
        query5 = db.query('''select * from tweets where tweets.user_id = $1 order by tweet_date_time''',session['id'])
        return render_template(
            'profile.html',
            user = query1.namedresult()[0],
            tweets = query2.namedresult()[0],
            followee = query3.namedresult()[0],
            follower = query4.namedresult()[0],
            tweetcontent = query5.namedresult()
        )
    else:
        return redirect('/login')

@app.route('/timeline')
def timeline():
    if 'id' in session:
        query1 = db.query('''select * from users where users.id = $1''',session['id'])
        query2 = db.query('''select count(tweets.tweetid) from tweets inner join users on tweets.user_id = users.id where users.id = $1''',1)
        query3 = db.query('''select count(follow.id) from follow where follow.followee = $1''',session['id'])
        query4 = db.query('''select count(follow.id) from follow where follow.follower = $1''',session['id'])
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
            ''',session['id'])
        print query5.namedresult()
        return render_template(
            'timeline.html',
            user = query1.namedresult()[0],
            tweets = query2.namedresult()[0],
            followee = query3.namedresult()[0],
            follower = query4.namedresult()[0],
            timeline_tweets = query5.namedresult()
        )
    else:
        return redirect('/login')

@app.route('/signup')
def signup():
    return render_template(
    'signup.html',
    message = 'Please signup to continue'
    )

@app.route('/sign_up', methods=['POST'])
def sign_up():
    name = request.form['name']
    email = request.form['email']
    username = request.form['username']
    textpass = request.form['password']
    password =b"%r" %textpass
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
    query1 = db.query('''select exists(select 1 from users where email = $1)''', email)
    query2 = db.query('''select exists(select 1 from users where username = $1)''', username)
    if query1.namedresult()[0].exists:
        print query1.namedresult()[0].exists
        return render_template(
        'signup.html',
        message = 'Email exists in database'
        )
    elif query2.namedresult()[0].exists:
        return render_template(
        'signup.html',
        message = 'Username exists in database'
        )
    else:
        db.query('''insert into users values(default, $1, $2, $3, $4)''',name,email,username,hashed)
        return redirect(
        '/login',
        message = 'Welcome $1, please login!'
        )


@app.route('/login')
def login():
    return render_template(
    'login.html',
    message = 'Please login!'
    )

@app.route('/log_in', methods=['POST'])
def log_in():
    username = request.form['username']
    textpass = request.form['password']
    password =b"%r" %textpass
    query1 = db.query('''select * from users where users.username = $1''', username)
    if query1.namedresult()[0]:
        hashed = query1.namedresult()[0].password
        if bcrypt.hashpw(password, hashed) == hashed:
            print 'It matches!'
            session['id'] = query1.namedresult()[0].id
            session['name'] = query1.namedresult()[0].name
            return redirect('/')
        else:
            print 'It doesnt match'
            return redirect('/login',
            message = 'Username or password doesnt match'
            )
    return redirect('/')

@app.route('/resetpassword')
def resetpassword():
    pass
@app.route('/follow')
def follow():
    print 'follow'

@app.route('/like')
def like():
    print 'Like'

@app.route('/retweet')
def retweet():
    print 'Retweet'

app.secret_key = 'SJKD9230SKJB8U23KBSV76T32KJB975KKS83DSI29HD4TD7V'

if __name__ == '__main__':
    app.debug = True
    app.run(debug = True)
