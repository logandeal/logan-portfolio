import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime as dt
from playhouse.shortcuts import model_to_dict

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

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

load_dotenv()
app = Flask(__name__)

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

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

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

