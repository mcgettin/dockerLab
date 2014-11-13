# This script created a queue
#
# Author - Paul Doyle Aug 2013
#
#
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError

conn1 = boto.sqs.connect_to_region("us-east-1", aws_access_key_id='AKIAIR7EH3TNSTDUCWKA', aws_secret_access_key='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')
conn2 = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='AKIAIR7EH3TNSTDUCWKA', aws_secret_access_key='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')


rs = conn1.get_all_queues()
for q in rs:
	print q.id


rs = conn2.get_all_queues()
for q in rs:
	print q.id


