from flask import Flask
from flask import request
import os, sys
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return 'Index Page\n'

@app.route('/hello')
def hello():
	return 'Hello World\n'
  
@app.route('/user/<username>')
def show_user_profile(username):
# show the user profile for that user
	return 'User %s\n' % username

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

@app.route('/chkUploads')
def chk_uploads():
	path = "./uploads/"
	dirs = os.listdir( path )
	f_str=""
	for name in dirs:
		f_str +=(str)(name)+"\n"

	return f_str

@app.route('/eu1')
def run_eu1():
	i=0
	total=0
	
  	while i < 1000: #stop when we reach multiple bigger than 1000 
    		if(i%5==0 or i%3==0): #ie if multiple of 5 or 3
      			total+=i #add multiple to cumulative tally
        
      		i+=1 #next number (will be used only if a valid multiple)
  	
	result=" "+(str)(total)+"\n"		
  	return result

@app.route('/eu2')
def run_eu2():
	pre,fib,tally=0,1,0 #initialize variables, pre is last term fib is current
  	MAX=4000000 #4million is maximum value of a term

  	while fib <= MAX: 
    		if(fib%2): tally+=fib #add to tally is fib term is even
    		pre,fib=fib,pre+fib #get new values for pre and fib
  	
	result=" "+(str)(tally)+"\n"
  	return result

@app.route('/listqueues')
def listQueues():
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

        result=""
        rs = conn.get_all_queues()
        for q in rs:
                result=result + (str)(q.id) + "\n"
	return result

@app.route('/createQ/<name>')
def createQueue(name):
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

		
	if(len(name)>0):
		mkQ=conn.create_queue(name)
	else:
		return "Wrong number of arguments\n"
	return "queue created\n"

@app.route('/delQMsg/<name>')
def deleteMsg(name):
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

	#if the queue name is given: proceed
	if(len(name) > 0):
		q = conn.get_queue(name) #queue name in argv
		msg = q.get_messages()[0] #gets next message
		msg.get_body()
		q.delete_message(msg) #deletes that retrieved message
		return "message deleted\n"
	else:
		return "FAIL: A name is needed (as argument) for the Queue.\n"

@app.route('/readQMsg/<name>')
def readMsg(name):
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

	#if the queue name is given: proceed
	if(len(name) > 0):
		q = conn.get_queue(name) #queue name in argv
		rd = q.get_messages()
		if len(rd) > 0: #while there are messages on queue
			return rd[0].get_body()
		else: return "Queue has no more messages\n"
	else:
		return "FAIL: A name is needed (as argument) for the Queue.\n"


@app.route('/numQMsg/<name>')
def countMsg(name):
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

	#if the queue name is given: proceed
	if(len(name) > 0):
		q = conn.get_queue(name) #queue name in argv
		num = q.count()
		if (num > 0): return "No. of messages: "+str(num)+"\n"
		else: return "No messages on queue\n"
	else:
		return "FAIL: A name is needed (as argument) for the Queue.\n"

@app.route('/manyQMsg/<name>')
def manyMsg(name):
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

	if(len(name) > 0):
		q = conn.get_queue(name)
		txt = Message()
		for i in range(100): #make 100 messages (set + write)
			gen="auto-gen msg no."+str(i+1)
			txt.set_body(gen)
			q.write(txt)
		return "wrote many messages\n"
	else:
		return "FAIL: A name is needed (as argument) for the Queue.\n"

@app.route('/writeQMsg/<name>/<msg>')
def writeMsg(name,msg):	
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

	if(len(name) > 0 and len(msg) > 0):
		q = conn.get_queue(name)
		txt = Message()
		txt.set_body(msg)
		q.write(txt)
		return "wrote message\n"
	else:
		return "FAIL: A name and a message is needed (as arguments) for the Queue.\n"


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
