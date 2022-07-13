import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime as dt
from playhouse.shortcuts import model_to_dict
from libgravatar import Gravatar

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=dt.datetime.now)
    pic_url = TextField()

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])



@app.route('/')
def index():
    return render_template('index.html', title="TyRoyLog Portfolio", url=os.getenv("URL"))

@app.route('/tylerswork/')
def tylerwork():
    return render_template('tylerwork.html')
    
@app.route('/tylershobbies/')
def tylerhobby():
    return render_template('tylerhobby.html')

@app.route('/loganswork/')
def loganwork():
    return render_template('loganwork.html')

@app.route('/loganshobbies/')
def loganhobby():
    return render_template('loganhobby.html')

@app.route('/royswork/')
def roywork():
    return render_template('roywork.html')

@app.route('/royshobbies/')
def royhobby():
    return render_template('royhobby.html')

@app.route('/aboutus/')
def aboutus():
    return render_template('aboutus.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', timeline=TimelinePost.select().order_by(TimelinePost.created_at.desc()))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    # Validate name
    try:
        name = request.form['name']
        if len(name) < 1:
            return "Invalid content", 400
    except KeyError as err:
        return "Invalid name", 400

    # Validate email
    try:
        email = request.form['email']
        if "@" not in email:
            return "Invalid email", 400
    except KeyError as err:
        return "Invalid email", 400

    # Validate content
    try:
        content = request.form['content']
        if len(content) < 1:
            return "Invalid content", 400
    except KeyError as err:
        return "Invalid content", 400
    
    g = Gravatar(email)
    gravatar_url = g.get_image()
    timeline_post = TimelinePost.create(name=name, email=email, content=content, pic_url=gravatar_url)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['GET'])
def get_time_line_post_by_id(post_id):
    return model_to_dict(
      TimelinePost.select().where(TimelinePost.id == post_id)[0]
    )

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post_by_id(post_id):
    TimelinePost.delete_by_id(post_id)
    return "deleted post " + post_id

#@app.route('/api/timeline_post', methods=['DELETE'])
#def delete_time_line():
#        model_to_dict(p)
#        for p in
#    TimelinePost.delete_by_id()
#        ]
#    }

if __name__ ==  "__main__":
    app.run()

