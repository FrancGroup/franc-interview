import json
from datetime import datetime
from flask import Flask, render_template, jsonify, Response, request

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    return render_template('index.html', username = username)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

@app.route('/example') # Views a twwet from kyle
def display_tweets():
    with open('./posts.json', 'r') as f:
        posts = f.read()
        posts_dict = json.loads(posts)
        return Response(str(posts_dict['Kyle']), mimetype="application/json")

class Tweet:
    def __init__(self, txt, date):
        self.txt = txt
        self.date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

def tweetListToString(Tlist): # converts Tweet object list to str list
    new_list = []
    for T in Tlist:
        string = T.txt + " "+ str(T.date)
        new_list.append(string)
    return new_list

@app.route('/tweets', methods=['POST','GET'])
def display_timeline():
    tweetlist = []
    username = request.form['users'] # get selected user

    f_users = open('./users.json', 'r') # read all users
    users = f_users.read()
    users_dict = json.loads(users)

    f_posts = open('./posts.json', 'r') # read all posts
    posts = f_posts.read()
    post_dict = json.loads(posts)

    for tweets in post_dict[username]: # append user's tweets
            if tweets['status']:
                t = Tweet(tweets['status'], tweets['time'] )
                tweetlist.append(t)

    for followers in users_dict[username]: # append followers tweet
        for tweet in post_dict[followers]:
            if tweet['status']:
                t = Tweet(tweet['status'], tweet['time'] )
                tweetlist.append(t)
                
    tweetlist.sort(key=lambda tweet: tweet.date) # sort tweets by date
    new_tlist = tweetListToString(tweetlist) # convert tweets to string
    return render_template('index.html', tweetlist = new_tlist)

if __name__ == '__main__':
    app.run(host='127.0.0.1')