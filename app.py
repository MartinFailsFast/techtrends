import sqlite3
import logging
#import subprocess
#from wsgiref.simple_server import WSGIRequestHandler
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
#from werkzeug.middleware.dispatcher import DispatcherMiddleware
#from werkzeug.serving import run_simple


# Variable to count DB requests
conCount= 0



# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global conCount
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conCount +=1
    return connection

# Function to get a post using its ID
def get_post(post_id):   
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    app_logger.info(f'Article "{post["title"]}" retrieved!')
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# Healthcchek endpoint
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

# Metric endpoint 
# Response Format: {"db_connection_count": 1, "post_count": 7}
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    dbCount = connection.execute('SELECT count(*) FROM posts').fetchone()[0]
    connection.close()
    response = app.response_class(
            response=json.dumps({"db_connection_count": dbCount, "post_count": conCount}),
            status=200,
            mimetype='application/json'
    )
    return response


# Define the first log format for Werkzeug
werkzeug_format = '%(levelname)s:%(name)s:%(message)s'
werkzeug_formatter = logging.Formatter(werkzeug_format)


# Define the second log format for your application
app_format = '%(levelname)s:%(name)s:%(asctime)s, %(message)s'
app_formatter = logging.Formatter(app_format, datefmt='%d/%m/%Y, %H:%M:%S')

# Create a logger for Werkzeug
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# Create a console handler for Werkzeug
werkzeug_handler = logging.StreamHandler()
werkzeug_handler.setFormatter(werkzeug_formatter)
werkzeug_logger.addHandler(werkzeug_handler)

# Create a logger for your application
app_logger = logging.getLogger('app')
app_logger.setLevel(logging.INFO)

# Create a console handler for your application
app_handler = logging.StreamHandler()
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)
 

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
