from fastapi import FastAPI
import redis

app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/users/{user_id}/stats")
def get_user_stats(user_id: str):
    key = f"user:{user_id}"
    return {
        "user_id": user_id,
        "order_count": int(redis_client.hget(key, "order_count") or 0),
        "total_spend": float(redis_client.hget(key, "total_spend") or 0.0)
    }

@app.get("/stats/global")
def get_global_stats():
    key = "global:stats"
    return {
        "total_orders": int(redis_client.hget(key, "total_orders") or 0),
        "total_revenue": float(redis_client.hget(key, "total_revenue") or 0.0)
    }
