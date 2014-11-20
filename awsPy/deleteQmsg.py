# This script deletes a queue's message
#
# Author - mcgettin
#
#
import sys # for reading from argv
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError

conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xxIAINXYPLZEZUALDFYQ', aws_secret_access_key='xxfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

#if the queue name is given: proceed
if(len(sys.argv) == 2):
	q = conn.get_queue(sys.argv[1]) #queue name in argv
	msg = q.get_messages()[0] #gets next message
	msg.get_body()
	q.delete_message(msg) #deletes that retrieved message
else:
	print("FAIL: A name is needed (as argument) for the Queue.")

