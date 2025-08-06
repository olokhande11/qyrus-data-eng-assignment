import boto3
import json
import os
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'



sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')

# Create Queue
queue_url = sqs.create_queue(QueueName='order-queue')['QueueUrl']



# Sample Order Message
order = {
    "order_id": "ORD1234",
    "user_id": "U5678",
    "order_timestamp": "2024-12-13T10:00:00Z",
    "order_value": 99.99,
    "items": [
        {"product_id": "P001", "quantity": 2, "price_per_unit": 20.00},
        {"product_id": "P002", "quantity": 1, "price_per_unit": 59.99}
    ],
    "shipping_address": "123 Main St, Springfield",
    "payment_method": "CreditCard"
}

# Send message
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps(order)
)
