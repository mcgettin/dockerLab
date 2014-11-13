# This script read a queue's messages
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

conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='AKIAIR7EH3TNSTDUCWKA', aws_secret_access_key='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')

#if the queue name is given: proceed
if(len(sys.argv) == 2):
	q = conn.get_queue(sys.argv[1]) #queue name in argv
	rd = q.get_messages()
	if len(rd) > 0: #while there are messages on queue
		print(rd[0].get_body())
	else: print("Queue has no more messages")
else:
	print("FAIL: A name is needed (as argument) for the Queue.")

