from flask import Flask, render_template, request, redirect, session

import pg
import bcrypt

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

db = pg.DB(
dbname=os.environ.get('DBNAME'),
host=os.environ.get('DBHOST'),
port=int(os.environ.get('DBPORT')),
user=os.environ.get('DBUSER'),
passwd=os.environ.get('DBPASSWORD')
)

app = Flask('ChirpApp')

@app.route('/')
def home():
    query1 = db.query('''select * from tweets inner join users on users.id = tweets.user_id order by tweets.tweet_date_time''')
    return render_template(
    'home.html',
    tweets = query1.namedresult()
    )


@app.route('/profile')
def profile():
    if 'id' in session:
        query1 = db.query('''select * from users where users.id = $1''',session['id'])
        query2 = db.query('''select count(tweets.tweetid) from tweets inner join users on tweets.user_id = users.id where users.id = $1''',session['id'])
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
        query5 = db.query('''select timeline.tweetid, timeline.tweet_content, timeline.tweet_date_time, users.username, timeline.likes, timeline.retweet_num,timeline.retweet_user_name from (select tweets.tweetid, tweets.tweet_content, tweets.tweet_date_time, tweets.user_id, tweets.likes, tweets.retweet_num, tweets.retweet_user_name from tweets
        inner join follow on tweets.user_id = follow.followee where follow.follower = $1 union select tweets.tweetid, tweets.tweet_content, tweets.tweet_date_time, tweets.user_id, tweets.likes, tweets.retweet_num,tweets.retweet_user_name from tweets where tweets.user_id = $1) as timeline inner join users on timeline.user_id = users.id order by tweet_date_time
        ''',session['id'])
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
        '/login'
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
            session['username'] = query1.namedresult()[0].username
            return redirect('/')
        else:
            print 'It doesnt match'
            return render_template('login.html',
            message = 'Username or password doesnt match'
            )
    return redirect('/')

@app.route('/users/<username>/settings')
def settings(username):
    pictures = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    return render_template(
    'settings.html',
    message = "Select your profile picture!",
    profile_pictures = pictures
    )

@app.route('/users/<username>/settings/update', methods=['POST'])
def update(username):
    picture = request.form['profile_picture']
    query1 = db.query('''update users set pic_id = $1 where users.username = $2''', picture, username)
    return redirect('/users/%s' %username)


@app.route('/users/<username>')
def user_profile(username):
    query = db.query('''select users.id from users where users.username = $1''',username)
    query1 = db.query('''select * from users where users.id = $1''',query.namedresult()[0].id)
    query2 = db.query('''select count(tweets.tweetid) from tweets inner join users on tweets.user_id = users.id where users.id = $1''',query.namedresult()[0].id)
    query3 = db.query('''select count(follow.id) from follow where follow.followee = $1''',query.namedresult()[0].id)
    query4 = db.query('''select count(follow.id) from follow where follow.follower = $1''',query.namedresult()[0].id)
    query5 = db.query('''select * from tweets where tweets.user_id = $1 order by tweet_date_time''',query.namedresult()[0].id)
    query6 = db.query('''select case when count(*) = 1 then TRUE else FALSE end from follow where follow.followee = $1 and follow.follower = $2''',query.namedresult()[0].id, session['id'])
    print query6.namedresult()[0].case
    return render_template(
        'profile.html',
        user = query1.namedresult()[0],
        tweets = query2.namedresult()[0],
        followee = query3.namedresult()[0],
        follower = query4.namedresult()[0],
        tweetcontent = query5.namedresult(),
        follow_status = query6.namedresult()[0].case
        )

@app.route('/resetpassword')
def resetpassword():
    print 'resetpassword'

@app.route('/follow/<username>', methods=['POST'])
def follow(username):
    query = db.query('''select users.id from users where users.username = $1''',username)
    query1 = db.query('''insert into follow values(default, $1, $2)''',session['id'],query.namedresult()[0].id)
    return redirect(request.referrer)

@app.route('/chirp', methods=['POST'])
def chirp():
    user_id = session['id']
    chirp = request.form['chirp']
    if chirp:
        db.query('''insert into tweets values(default, $1, default, $2, 0, 0, null)''',user_id, chirp)
        return redirect(
        '/profile'
        )

@app.route('/like_retweet', methods=['POST'])
def like():
    print request.form
    if request.form.get('likes'):
        print request.form['likes']
        the_likes = request.form['likes'].split(" ")
        if session['id'] and the_likes[1] != session['username'] and the_likes[0]:
            db.query('''update tweets set likes = likes + 1 where tweets.tweetid = $1''',the_likes[0])
            return redirect(request.referrer)

    elif request.form.get('retweets'):
        the_retweets = request.form['retweets'].split(" ")
        print the_retweets
        if session['id'] and the_retweets[1] != session['username'] and the_retweets[0]:
            query1 = db.query('''select tweets.tweet_content from tweets where tweets.tweetid = $1''',the_retweets[0])
            print query1.namedresult()[0].tweet_content
            db.query('''insert into tweets values(default, $1, default, $2, 0, 0, $3)''',session['id'], query1.namedresult()[0].tweet_content, the_retweets[1])
            db.query(''' update tweets set retweet_num = retweet_num + 1 where tweets.tweetid = $1''',the_retweets[0])
            print 'A retweet has occurred!'
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)
    return redirect(request.referrer)
@app.route('/unfollow/<username>', methods=['POST'])
def un_follow(username):
    db.query('''delete from follow where follow.followee = (select users.id from users where users.username = $1) and follow.follower = $2''',username, session['id'],)
    return redirect(request.referrer)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


app.secret_key = 'SJKD9230SKJB8U23KBSV76T32KJB975KKS83DSI29HD4TD7V'

if __name__ == '__main__':
    app.debug = True
    app.run(debug = True)
