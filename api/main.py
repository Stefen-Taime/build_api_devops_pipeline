from fastapi import FastAPI, HTTPException, Query
from starlette.middleware.gzip import GZipMiddleware
import httpx
from pydantic import BaseModel
from typing import List
from aiologger import Logger
import aioredis
import json
import asyncio

app = FastAPI()
#Payload Compression: 
app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses larger than 1KB

# Asynchronous Logging
logger = Logger.with_default_handlers()

REDIS_HOST = "192.168.2.19"
REDIS_PORT = "6379"
REDIS_PASSWORD = "admin"
REDIS_DB = 0  # Connects to the first database (DB 0)
CACHE_EXPIRE = 60  # Cache expiration time in seconds

class BankAccount(BaseModel):
    id: int
    uid: str
    account_number: str
    iban: str
    bank_name: str
    routing_number: str
    swift_bic: str
    user_id: str
    dt_current_timestamp: str

redis = None

# Data Caching
@app.on_event("startup")
async def startup_event():
    global redis
    redis = await aioredis.create_redis_pool(
        f"redis://{REDIS_HOST}:{REDIS_PORT}", 
        db=REDIS_DB
    )

async def get_all_bank_accounts():
    global redis
    # Try to get data from Redis cache
    cached_data = await redis.get('bank_accounts')
    if cached_data:
        await logger.info("Fetched data from Redis cache")
        return json.loads(cached_data)

    # If not in cache, fetch from source and cache it
    await logger.info("Fetching data from external source")
    url = "https://raw.githubusercontent.com/Stefen-Taime/open-source-data/main/bank/json/json_bank_20240116_1.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    await redis.set('bank_accounts', json.dumps(data), expire=CACHE_EXPIRE)
    return data

# Result Pagination
@app.get("/bank-accounts/", response_model=List[BankAccount])
async def read_bank_accounts(page: int = Query(1, alias="page"), page_size: int = Query(10, alias="page_size")):
    await logger.info(f"Fetching bank accounts page: {page} with page size: {page_size}")
    accounts = await get_all_bank_accounts()
    start = (page - 1) * page_size
    end = start + page_size
    return accounts[start:end]

@app.get("/bank-accounts/user/{user_id}", response_model=List[BankAccount])
async def read_bank_account_by_user_id(user_id: str, page: int = Query(1, alias="page"), page_size: int = Query(10, alias="page_size")):
    await logger.info(f"Fetching bank accounts for user_id: {user_id}, page: {page}, page size: {page_size}")
    accounts = await get_all_bank_accounts()
    filtered_accounts = [account for account in accounts if account['user_id'] == user_id]
    if not filtered_accounts:
        await logger.warning(f"No accounts found for user_id: {user_id}")
        raise HTTPException(status_code=404, detail="User ID not found")
    start = (page - 1) * page_size
    end = start + page_size
    return filtered_accounts[start:end]

@app.on_event("shutdown")
async def shutdown_event():
    global redis
    await logger.shutdown()
    redis.close()
    await redis.wait_closed()
