from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyBoLHj9lGeYp7xt_3f7otRsE831g9hEpcA",
  "authDomain": "help-441e0.firebaseapp.com",
  "projectId": "help-441e0",
  "storageBucket": "help-441e0.appspot.com",
  "messagingSenderId": "376818407257",
  "appId": "1:376818407257:web:efb817bd9381dfd9ca5e48",
  "databaseURL":"https://help-441e0-default-rtdb.firebaseio.com/"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except Exception as e:
            error = "Authentication failed"
            print(e)
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email' : email, 'full_name' : full_name, 'username' : username, 'bio' : bio}
            db.child('Users').child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except Exception as e:
            print(e)
            error = "Authentication failed"

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        UID = login_session['user']['localId']
        tweet = {'title' : title, 'text' : text}
        db.child('Tweets').push(tweet)

    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    tweets = db.child('Tweets').get().val()
    return render_template('tweet.html', tweets = tweets)


if __name__ == '__main__':
    app.run(debug=True)