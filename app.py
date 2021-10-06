from flask import Flask, render_template, jsonify, Response, request
import json
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    users = users_view()
    users = json.loads(users.data)

    if username == None:
        return render_template('index.html')
    else:

        users_followed = users[username]

        all_users = users_followed
        all_users.append(username)

        posts = posts_view()
        posts = json.loads(posts.data)
        
        tweets = []

        def sort_tweet(obj):
            return obj['time']

        for user in all_users:
            for tweet in posts[user]:
                time = tweet['time']
                time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
                time = time.strftime("%B %-d, %Y %-H:%M")

                tweets.append({
                    'user': user,
                    'tweet': tweet['status'],
                    'time': time
                })

        tweets.sort(key = sort_tweet)
        tweets.reverse()

        return render_template('index.html', username = username, tweets = tweets)

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

if __name__ == '__main__':
    app.run(host='127.0.0.1')