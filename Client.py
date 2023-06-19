import asyncio
from fastapi import FastAPI, HTTPException, WebSocket,Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import time
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]


class Client(BaseModel):
    macAddress: str
    firstName: str
    lastName: str
    age: int
    phone: str
    address: str
    
class VitalSigns(BaseModel):
    macAddress: str
    timestamp: int
    bloodPressure: str
    bodyTemperature: float
    heartBeat: int

        
app = FastAPI(middleware=middleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient("mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/")
db = client.get_database('HealthTracking')
collection = db.get_collection('Client')
vital_signs_collection = db.get_collection('vitalSigns')

@app.post("/clients/")
async def create_client(client: Client):
    # Insert the client data into the MongoDB collection
    client_dict = client.dict()
    result = await collection.insert_one(client_dict)
    client_id = result.inserted_id
    print(Client)
    # Return the client with ID
    return {**client.dict(), "id": str(client_id)}

@app.get("/clients/{client_id}")
async def read_client(client_id: str):
    # Get client by ID
    client_data = await collection.find_one({"_id": client_id})
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found")

    return client_data


@app.get("/vitalsigns/average/{mac_address}")
async def average_vital_signs(mac_address: str):
    # First, fetch the client using the macAddress
    client_data = await collection.find_one({"macAddress": mac_address})
    print(client_data)

    # If the client doesn't exist, return an error
    if client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get the current timestamp in Unix time
    current_time = time.time()

    # Calculate the timestamp for five minutes ago
    five_minutes_ago = current_time - 5*60

    # Query the MongoDB collection for all records within the last five minutes
    records = vital_signs_collection.find({
        "userId": str(client_data["_id"]),
        "timestamp": {"$gte": five_minutes_ago}
    })

    # Calculate the average blood pressure, body temperature, and heart beat
    total_pressure = 0
    total_temperature = 0.0
    total_heartbeat = 0
    count = 0
    async for record in records:
        total_pressure += int(record['bloodPressure'])
        total_temperature += record['bodyTemperature']
        total_heartbeat += record['heartBeat']
        count += 1

    # If no records are found, return an error message
    if count == 0:
        raise HTTPException(status_code=404, detail="No records found for client within the last 5 minytes ." )

    average_pressure = total_pressure / count
    average_temperature = total_temperature / count
    average_heartbeat = total_heartbeat / count

    # Return the averages
    return {
        "averageBloodPressure": average_pressure,
        "averageBodyTemperature": average_temperature,
        "averageHeartBeat": average_heartbeat
    }




@app.get("/vitalsigns/average/{mac_address}/{time_interval}")
async def average_vital_signs(mac_address: str, time_interval):
    
    # First, fetch the client using the macAddress
    client_data = await collection.find_one({"macAddress": mac_address})
    print(client_data)

    # If the client doesn't exist, return an error
    if client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get the current timestamp in Unix time
    current_time = time.time()

    # Calculate the timestamp for the start of the time interval
    if time_interval == "5min":
        start_time = current_time - timedelta(minutes=5).total_seconds()
    elif time_interval == "1hour":
        start_time = current_time - timedelta(hours=1).total_seconds()
    elif time_interval == "1day":
        start_time = current_time - timedelta(days=1).total_seconds()
    elif time_interval == "1week":
        start_time = current_time - timedelta(weeks=1).total_seconds()
    elif time_interval == "1month":
        start_time = current_time - timedelta(days=30).total_seconds()  # assuming a month is 30 days
    else:
        raise HTTPException(status_code=400, detail="Invalid time interval")

    # Query the MongoDB collection for all records within the time interval
    records = vital_signs_collection.find({
        "userId": str(client_data["_id"]),
        "timestamp": {"$gte": start_time}
    })

    # Calculate the average blood pressure, body temperature, and heart beat
    total_pressure = 0
    total_temperature = 0.0
    total_heartbeat = 0
    count = 0
    async for record in records:
        total_pressure += int(record['bloodPressure'])
        total_temperature += record['bodyTemperature']
        total_heartbeat += record['heartBeat']
        count += 1

    # If no records are found, return an error message
    if count == 0:
        raise HTTPException(status_code=404, detail="No records found for client within the time interval")

    average_pressure = total_pressure / count
    average_temperature = total_temperature / count
    average_heartbeat = total_heartbeat / count

    # Return the averages
    return {
        "averageBloodPressure": average_pressure,
        "averageBodyTemperature": average_temperature,
        "averageHeartBeat": average_heartbeat
    }

@app.websocket("/ws/vitalsigns/average/{mac_address}/{duration}")
async def websocket_endpoint(websocket: WebSocket, mac_address: str, duration: str):
    await websocket.accept()

    while True:
        # Fetch the client using the macAddress
        client_data = await collection.find_one({"macAddress": mac_address})

        # If the client doesn't exist, close the connection
        if client_data is None:
            await websocket.close(code=1000)
            break

        # Get the current timestamp in Unix time
        current_time = time.time()

        # Define the duration mappings
        duration_mapping = {
            '5min': 5 * 60,  # 5 minutes
            '1hour': 60 * 60,  # 1 hour
            '1day': 24 * 60 * 60,  # 1 day
            '1month': 30 * 24 * 60 * 60  # 1 month (approximately)
        }

        # Validate the duration parameter
        if duration not in duration_mapping:
            await websocket.close(code=1000)  # You can use a different status code for invalid parameters
            break

        # Calculate the timestamp for the specified duration ago
        duration_ago = current_time - duration_mapping[duration]

        # Query the MongoDB collection for all records within the last specified duration
        records = await vital_signs_collection.find({
            "userId": str(client_data["_id"]),
            "timestamp": {"$gte": duration_ago}
        }).to_list(None)

        # Check if the records list is empty
        if len(records) == 0:
            await websocket.close(code=1000)
            break

        # Prepare a list to hold the data for each record
        record_data = []

        # Iterate over the records and prepare the data
        for record in records:
            record_data.append({
                "time": record['timestamp'],
                "bloodPressure": record['bloodPressure'],
                "bodyTemperature": record['bodyTemperature'],
                "heartBeat": record['heartBeat']
            })

        # Send the data for each record
        await websocket.send_json(record_data)

        # Wait for a while before next iteration
        await asyncio.sleep(15)  # Modify this sleep duration as per your needs.

