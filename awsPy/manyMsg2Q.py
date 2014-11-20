# This script created 100 messages on a queue
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


if(len(sys.argv) == 2):
	q = conn.get_queue(sys.argv[1])
	txt = Message()
	for i in range(100): #make 100 messages (set + write)
		gen="auto-gen msg no."+str(i+1)		
		txt.set_body(gen)
		q.write(txt)
else:
	print("FAIL: A name is needed (as argument) for the Queue.")

