# 📦 Data Engineer Assignment – Order Processing System

This project is part of a Data Engineering assignment that simulates a distributed **order processing system** using microservices architecture. It demonstrates how a web service and background worker interact via AWS SQS (emulated using LocalStack) and Redis for data storage.

---

## 📁 Project Structure

Qyrus_data_eng/
├── app/ # FastAPI service
│ └── main.py
├── worker/ # SQS worker
│ └── worker.py
├── scripts/ # Utility scripts
│ └── populate_sqs.py # Push test messages to SQS
├── Dockerfile # For the worker container
├── docker-compose.yml # Docker setup
├── requirements.txt # Dependencies
└── README.md # Project documentation



---

## ⚙️ Technologies Used

- **FastAPI** – RESTful web API
- **Redis** – In-memory data storage
- **LocalStack** – AWS service emulator (used for SQS)
- **boto3** – AWS SDK for Python
- **Docker & Docker Compose** – Container orchestration

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Qyrus_data_eng


2. Start all services

docker-compose build
docker-compose up


This will start:

FastAPI app at http://localhost:8000

Redis

LocalStack with SQS

SQS Worker

python scripts/populate_sqs.py


4. Verify if messages were processed

curl http://localhost:8000/stats/global


Expected output (after processing):


{
  "total_orders": 10,
  "total_revenue": 10000.0
}



🐛 Troubleshooting Tips
If you see this error:

arduino
Copy
Edit
❌ Failed to create/get queue: Could not connect to the endpoint URL: ...


✅ Solution:

Make sure LocalStack is healthy and running

Set AWS credentials in the terminal:

bash
Copy
Edit
set AWS_ACCESS_KEY_ID=test
set AWS_SECRET_ACCESS_KEY=test
Ensure populate_sqs.py and worker.py use:

python
Copy
Edit
endpoint_url="http://localstack:4566"
region_name="us-east-1"
✅ Tasks Completed

✅ Tasks Completed
 FastAPI service with analytics endpoint (/stats/global)

 Redis used for data aggregation

 SQS worker implemented to process messages

 LocalStack used to mock AWS SQS

 Script to populate messages to queue

 Docker Compose setup for all services

 Final output verified using curl command

🙋‍♂️ Submitted by
Omkar Lokhande
omkar.ds.tech@gmail.com




