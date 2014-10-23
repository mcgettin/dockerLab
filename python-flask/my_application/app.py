from flask import Flask
from flask import request
import os, sys
app = Flask(__name__)

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
def hello():
	return 'Hello World'
  
@app.route('/user/<username>')
def show_user_profile(username):
# show the user profile for that user
	return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
# show the post with the given id, the id is an integer
	return 'Post %d' % post_id

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save('./uploads/'+f.filename)
	return '',201

@app.route('/chkUploads',methods =['GET', 'POST'])
def chk_uploads():
	path = "./uploads/"
	dirs = os.listdir( path )
	f_str=""
	for name in dirs:
		f_str +=(str)(name)+"\n"

	return f_str
    

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
