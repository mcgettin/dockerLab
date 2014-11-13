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

conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='AKIAIR7EH3TNSTDUCWKA', aws_secret_access_key='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')


if(len(sys.argv) > 2):
	q = conn.get_queue(sys.argv[1])
	txt = Message()
	for i in range(100): #make 100 messages (set + write)
		txt.set_body("auto-gen msg no."+str(i+1))
		q.write(txt)
else:
	print("FAIL: A name is needed (as argument) for the Queue.")

