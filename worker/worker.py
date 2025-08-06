import boto3
import redis
import json
import time
import os

import os

# Inject credentials for LocalStack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

sqs = boto3.client(
    'sqs',
    endpoint_url='http://sqs.us-east-1.localstack.cloud:4566'
)

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Wait for Localstack to be fully ready
time.sleep(5)

# Get or create SQS queue
try:
    queue_url = sqs.create_queue(QueueName='order-queue')['QueueUrl']
    print(f"✅ Queue URL: {queue_url}")
except Exception as e:
    print(f"❌ Failed to create/get queue: {e}")
    exit(1)

print("🚀 Worker is now polling for messages...")

def validate_order(order):
    required_keys = ['order_id', 'user_id', 'order_value', 'items']
    for key in required_keys:
        if key not in order:
            print(f"❌ Missing key: {key}")
            return False

    # Validate order value
    try:
        calculated = sum(item['quantity'] * item['price_per_unit'] for item in order['items'])
        if abs(calculated - order['order_value']) > 0.01:
            print(f"❌ Order value mismatch: Expected {calculated}, Got {order['order_value']}")
            return False
    except Exception as e:
        print(f"❌ Error validating order: {e}")
        return False

    return True

def process_order(order):
    user_id = order['user_id']
    order_value = order['order_value']
    user_key = f"user:{user_id}"
    global_key = "global:stats"

    redis_client.hincrby(user_key, "order_count", 1)
    redis_client.hincrbyfloat(user_key, "total_spend", order_value)
    redis_client.hincrby(global_key, "total_orders", 1)
    redis_client.hincrbyfloat(global_key, "total_revenue", order_value)

    print(f"✅ Processed order {order['order_id']} for user {user_id}")

while True:
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=3
        )
        messages = response.get("Messages", [])
        if not messages:
            print("⏳ No messages received.")
        for msg in messages:
            body = json.loads(msg["Body"])
            print(f"📦 Received order: {body}")
            if validate_order(body):
                process_order(body)
            else:
                print(f"⚠️ Invalid order: {body}")

            # Delete message from queue
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
    except Exception as e:
        print(f"❌ Error in worker loop: {e}")
    time.sleep(1)