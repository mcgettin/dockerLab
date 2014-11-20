# This script lists all queues in eu-west-1
#
# Author - mcgettin
#
#
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError

#conn1 = boto.sqs.connect_to_region("us-east-1", aws_access_key_id='xxIAINXYPLZEZUALDFYQ', aws_secret_access_key='xxfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')
conn2 = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id='xxIAINXYPLZEZUALDFYQ', aws_secret_access_key='xxfZms2LJR39mi/W3eWBSGs0rD6dgfC9Q8lcCPRV')

'''
rs = conn1.get_all_queues()
for q in rs:
	print q.id
'''

rs = conn2.get_all_queues()
for q in rs:
	print q.id


