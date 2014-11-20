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

conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xxKIAINXYPLZEZUALDFYQ', aws_secret_access_key='xxfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')


if(len(sys.argv) == 2): # making sure there is a name arg given
	mkQ = conn.create_queue(sys.argv[1]) #use that arg
else:
	print("FAIL: A name is needed (as argument) for the Queue.")

