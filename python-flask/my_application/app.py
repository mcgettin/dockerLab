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

#curl examples are shown with te hash comment, above functions

'''default route, when just the ip is inserted after curl command
'''
#curl 172.17.0.xxx
@app.route('/')
def index():
	return 'Index Page\n'


'''simply returns a string
'''
#curl 172.17.0.xxx/hello
@app.route('/hello')
def hello():
	return 'Hello World\n'

  
'''grabs input from the user afer the ip and slash
'''
#curl 172.17.0.xxx/user/Bobby
@app.route('/user/<username>')
def show_user_profile(username):
	return 'User %s\n' % username


'''grabs user input as before, BUT casts it as an int
'''
#curl 172.17.0.xxx/post/5
@app.route('/post/<int:post_id>')
def show_post(post_id):
	return 'Post %d' % post_id #user input in place of %d


'''uploading file via POST request
'''
#curl -F @file=newFile.txt 172.17.0.xxx/upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file'] #in curl: @file= 
		f.save('./uploads/'+f.filename) #save file to /uploads dir
	return '',201 #CREATED status code


'''prints out all files in the directory /uploads
'''
#curl 172.17.0.xxx/chkUploads
@app.route('/chkUploads')
def chk_uploads():
	path = "./uploads/"
	dirs = os.listdir( path ) #stores dirs in the path 
	f_str=""
	for name in dirs: #print each dir from that directory 
		f_str +=(str)(name)+"\n"

	return f_str


'''euler solution 1
'''
#curl 172.17.0.xxx/eu1
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


'''euler solution 2
'''
#curl 172.17.0.xxx/eu2
@app.route('/eu2')
def run_eu2():
	pre,fib,tally=0,1,0 #initialize variables, pre is last term fib is current
  	MAX=4000000 #4million is maximum value of a term

  	while fib <= MAX: 
    		if(fib%2): tally+=fib #add to tally is fib term is even
    		pre,fib=fib,pre+fib #get new values for pre and fib
  	
	result=" "+(str)(tally)+"\n"
  	return result


'''lists all the queues in EU West (Ireland)
'''
#curl 172.17.0.xxx/listqueues
@app.route('/listqueues')
def listQueues():
	#connecting to region
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

        result=""
        rs = conn.get_all_queues() #store name of all queues
        for q in rs: #store each in its own line
                result=result + (str)(q.id) + "\n"
	return result


'''Create an sqs queue, using POST request via curl
'''
#curl -d "name=newQ" 172.17.0.xxx/createQ
@app.route('/createQ', methods=['GET', 'POST'])
def createQueue():
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')
	if(request.method=='POST'):
		mkQ=conn.create_queue(request.form['name'])#using request
	else:
		return "Wrong number of arguments\n"
	return "queue created\n"


'''delete a message on a queue, wose name is specified by the user
'''
#curl 172.17.0.xxx/delQMsg/newQ
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


'''read a message on the queue given by user input
'''
#curl 172.17.0.xxx/readQMsg/newQ
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


'''shows the number of messaes on a queue
'''
#curl 172.17.0.xxx/numQMsg/newQ
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


'''prints 100 generic messages on a queues
'''
#curl 172.17.0.xxx/manyQMsg/newQ
@app.route('/manyQMsg/<name>')
def manyMsg(name):
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

	if(len(name) > 0):
		q = conn.get_queue(name)
		txt = Message()
		for i in range(100): #make 100 messages (set + write)
			gen="auto-gen msg no."+str(i+1)
			txt.set_body(gen) #set the message txt via string
			q.write(txt) #write it to the queue
		return "wrote many messages\n"
	else:
		return "FAIL: A name is needed (as argument) for the Queue.\n"


'''prints user's message to a queue specified by the user
'''
#curl -d "name=newQ&message=Howdy!" 1721.7.0.xxx/writeQMsg
@app.route('/writeQMsg/',methods=['GET','POST'])
def writeMsg():	
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')
	#while a queue name is given and message is given too
	if(request.method=='POST'):
		q = conn.get_queue(request.form['name'])
		txt = Message() #set variable txt as a Message
		txt.set_body(request.form['message'])
		q.write(txt)
		return "wrote message\n"
	else:
		return "FAIL: A name and a message is needed (as arguments) for the Queue.\n"


''' deletes a queue via curl
'''
#curl -d "name=newQ" 172.17.0.xxx/deleteQ 
@app.route('/deleteQ', methods=['GET', 'POST'])
def delQ():
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xqfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')
  
  	#if the queue name is given: proceed
  	if(request.method=='POST'):
		conn.delete_queue(request.form['name']) #queue name is specified via POSTed request
	  	return "Queue deleted"
  	else:
		return "FAIL: A name is needed (as argument) for the Queue."



if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
