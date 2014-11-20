# This script created a queue
#
# Author - mcgettin
#
#
import sys
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError

conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xxIAINXYPLZEZUALDFYQ', aws_secret_access_key='xxfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

msg=""
args=len(sys.argv)

if(args > 2):
	q = conn.get_queue(sys.argv[1])
	txt = Message()
	
	for i in range(2,args):
		msg+=sys.argv[i]+" "
	txt.set_body(msg)
	q.write(txt)
else:
	print("FAIL: A name and a  message is needed (as arguments) for the Queue.")

