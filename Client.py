import asyncio
from fastapi import FastAPI, HTTPException, WebSocket,Path,Depends,status,BackgroundTasks,WebSocketDisconnect
from fastapi.responses import StreamingResponse,JSONResponse
from starlette.websockets import WebSocketDisconnect

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel,Field
from typing import Optional,List
from datetime import datetime, timedelta
import time
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
from collections import Counter
import json




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
    id: Optional[str]
    _id: Optional[str]
    macAddress: str
    firstName: str
    lastName: str
    age: int
    phone: str
    address: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    
class VitalSigns(BaseModel):
    macAddress: str
    timestamp: int
    bloodPressure: float
    bodyTemperature: float
    heartBeat: int

class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    password: Optional[str] = Field(alias='hashed_password')
    hashed_password: Optional[str] = None



class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class Item(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')
    # your other fields here

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True



        
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
admin = db.get_collection('admin')
vital_signs_collection=db.get_collection('vitalSigns')
alerts_collection = db['Alerts']




@app.get("/vitalsigns/average/{mac_address}")
async def average_vital_signs(mac_address: str):
    # First, fetch the client using the macAddress
    client_data = await collection.find_one({"macAddress": mac_address})
    print(client_data)
    first_name=client_data['firstName']
    last_name=client_data['lastName']

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
        "averageHeartBeat": average_heartbeat,
        "firstName": first_name,
        "lastName": last_name
    }




@app.get("/vitalsigns/average/{mac_address}/{time_interval}")
async def average_vital_signs(mac_address: str, time_interval):
    
    # First, fetch the client using the macAddress
    client_data = await collection.find_one({"macAddress": mac_address})
    print(client_data)
    first_name=client_data['firstName']
    last_name=client_data['lastName']


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
        "averageHeartBeat": average_heartbeat,
        "firstName": first_name,
        "lastName": last_name

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
        await asyncio.sleep(30)  # Modify this sleep duration as per your needs.




## auth 

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000000000



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str):
    user_doc = await admin.find_one({"username": username})
    if user_doc:
        user = UserInDB(**user_doc)
        return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/users/", response_model=User)
async def create_user(user: UserInDB):
    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Create a new user document
    user_doc = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "disabled": user.disabled,
        "hashed_password": hashed_password,
    }

    # Insert the new user into the MongoDB collection
    result = await admin.insert_one(user_doc)

    if result:
        return User(**user_doc)
    else:
        raise HTTPException(status_code=400, detail="User not created")

@app.post("/clients")
async def create_client(client: Client, current_user: User = Depends(get_current_user)):
    # Insert the client data into the MongoDB collection
    client_dict = client.dict()
    result = await collection.insert_one(client_dict)
    client_id = result.inserted_id
    # Return the client with ID
    return {**client.dict(), "id": str(client_id)}


#get all clients
@app.get("/clients", response_model=List[Client])
async def get_all_clients(current_user: User = Depends(get_current_user)):
    clients = []
    async for client in collection.find():
        client['id'] = str(client['_id'])
        clients.append(Client(**client))
    return clients



@app.delete("/clients/{client_id}")
async def delete_client(client_id: str, current_user: User = Depends(get_current_user)):
    result = await collection.delete_one({"_id": ObjectId(client_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}




    
#update client 


@app.put("/clients/{client_id}")
async def update_client(client_id: str, updated_client: Client, current_user: User = Depends(get_current_user)):
    existing_client = await collection.find_one({"_id": ObjectId(client_id)})
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    updated_client_dict = updated_client.dict(exclude_unset=True)
    await collection.update_one(
        {"_id": ObjectId(client_id)},
        {"$set": updated_client_dict}
    )






@app.get("/clients/{client_id}")
async def read_client(client_id: str, current_user: User = Depends(get_current_user)):
    # Get client by ID
    client_data = await collection.find_one({"_id": ObjectId(client_id)})
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found")

    # Convert ObjectId to str for JSON serialization
    client_data["_id"] = str(client_data["_id"])

    return client_data


conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'group2', 'auto.offset.reset': 'earliest'}
consumer = Consumer(conf)
consumer.subscribe(['alerts_topic'])
# Keep track of the last alert timestamp
last_timestamp = None
# Custom JSON encoder
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

async def get_new_alerts():
    global last_timestamp

    # If last_timestamp is None, this is the first time we are fetching alerts
    # In this case, we just update the last_timestamp and do not return any alerts
    if last_timestamp is None:
        last_alert = await alerts_collection.find().sort('timestamp', -1).to_list(length=1)
        if last_alert:
            last_timestamp = last_alert[0]['timestamp']
        return []

    # Find alerts which have a timestamp greater than the last_timestamp
    new_alerts = await alerts_collection.find({'timestamp': {'$gt': last_timestamp}}).sort('timestamp', -1).to_list(length=None)

    # Update the last_timestamp to the timestamp of the newest alert
    if new_alerts:
        last_timestamp = new_alerts[0]['timestamp']

    return new_alerts

@app.websocket("/alertos")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            new_alerts = await get_new_alerts()

            # Send new alerts to the client
            for alert in new_alerts:
                alert_json = JSONEncoder().encode(alert)
                await websocket.send_text(alert_json)

            # Wait for a while before checking for new alerts
            await asyncio.sleep(15)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


'''conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'group2', 'auto.offset.reset': 'earliest'}
consumer = Consumer(conf)
consumer.subscribe(['alerts_topic'])'''



@app.get("/getalerts")
async def get_all_alerts():
    client = MongoClient('mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/')
    db = client['HealthTracking']
    alerts_collection = db['Alerts']
    alerts = list(alerts_collection.find())

    for alert in alerts:
        alert["_id"] = str(alert["_id"])  # Convert ObjectId to string

    return alerts

@app.post("/markasread")
async def mark_all_as_read():
    client = MongoClient('mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/')
    db = client['HealthTracking']
    alerts_collection = db['Alerts']

    result = alerts_collection.update_many({}, {'$set': {'isRead': True}})
    
    return {"updated_count": result.modified_count}



@app.get("/unread-count")
async def get_unread_count():
    async def event_stream():
        while True:
            client = MongoClient('mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/')
            db = client['HealthTracking']
            alerts_collection = db['Alerts']

            count = alerts_collection.count_documents({"isRead": False})

            yield f"data: {json.dumps({'unread_count': count})}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(event_stream(), media_type="text/event-stream")



## stats
@app.get("/stats")
async def get_stats():
    # Get number of alerts of each type
    alerts = await alerts_collection.find().to_list(length=None)
    alert_types = [alert['alert'] for alert in alerts]
    alert_types_count = Counter(alert_types)

    # Define age groups
    age_groups = ['0-20', '20-40', '40-60', '60-80', '80-100']
    age_groups_result = {}

    # Get all clients
    clients = await collection.find().to_list(length=None)

    # Dividing clients by age group
    for age_group in age_groups:
        min_age, max_age = map(int, age_group.split('-'))
        clients_in_group = [client for client in clients if min_age <= client['age'] <= max_age]
        age_groups_result[age_group] = len(clients_in_group)



    # Get all alerts
    alerts = await alerts_collection.find().to_list(length=None)

    # Extract unique userIds from the alerts
    user_ids = list({ObjectId(alert['userId']) for alert in alerts})

    # Fetch all users that have triggered an alert
    users = await collection.find({'_id': {'$in': user_ids}}).to_list(length=None)

    # Build a mapping from user ObjectId to user document for efficient lookups
    user_map = {user['_id']: user for user in users}

    # Prepare a dictionary to store alert counts per age group
    age_groups_alerts = {age_group: 0 for age_group in age_groups}

    # Iterate over all alerts and increment the corresponding age group counter
    for alert in alerts:
        user = user_map[ObjectId(alert['userId'])]  # Get the user who triggered this alert
        user_age = user['age']  # Extract the user's age

        # Determine the age group of the user
        for age_group in age_groups:
            min_age, max_age = map(int, age_group.split('-'))
            if min_age <= user_age <= max_age:
                age_groups_alerts[age_group] += 1  # Increment the counter for this age group
                break  # No need to check other age groups
    

    stats = await db.command("dbstats")
    ## retutn only avgObjSize , dataSize , storageSize , indexSize ,indexes
    stats = {key: stats[key] for key in ['avgObjSize', 'dataSize', 'storageSize', 'indexSize', 'indexes']}


    return {"alert_types_count": alert_types_count, "age_groups_result": age_groups_result,"age_groups_alerts": age_groups_alerts,"stats":stats}
@app.on_event('startup')
async def startup_event():
    client = AsyncIOMotorClient('mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/')
    app.state.client_collection = client.db.get_collection('Client')
    app.state.vital_signs_collection = client.db.get_collection('vitalSigns')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await websocket.receive_text()
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed normally")
                break
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed unexpectedly")
                break

            vital_signs: VitalSigns = VitalSigns.parse_raw(data)
            print(f"Received data: {vital_signs}")

            client = await collection.find_one({'macAddress': vital_signs.macAddress})
            if client is None:
                print(f"No client found with macAddress {vital_signs.macAddress}")
                continue

            try:
                message = {
                    'userId': str(client['_id']),
                    'firstName': client['firstName'],
                    'lastName': client['lastName'],
                    'bloodPressure': vital_signs.bloodPressure,
                    'bodyTemperature': vital_signs.bodyTemperature,
                    'heartBeat': vital_signs.heartBeat,
                    'timestamp': vital_signs.timestamp  # UNIX timestamp
                }
            except KeyError as e:
                print(f"Missing field in client document: {e}")
                continue

            try:
                await vital_signs_collection.insert_one(message)
            except Exception as e:
                print(f"Error inserting document: {e}")
                continue

            # Check vital signs and insert alert to database if abnormal
            alert = None
            if vital_signs.bodyTemperature > 37.59:
                alert = {
                    'type': 'vital_signs_alert',
                    'alert': 'High temperature',
                    'value': vital_signs.bodyTemperature,
                    'isRead': False,
                    'userId': str(client['_id']),
                    'firstName': client['firstName'],
                    'lastName': client['lastName'],
                    'timestamp': vital_signs.timestamp
                }
            elif vital_signs.bloodPressure > 121 or vital_signs.bloodPressure < 78:
                alert = {
                    'type': 'vital_signs_alert',
                    'alert': 'Abnormal blood pressure',
                    'value': vital_signs.bloodPressure,
                    'isRead': False,
                    'userId': str(client['_id']),
                    'firstName': client['firstName'],
                    'lastName': client['lastName'],
                    'timestamp': vital_signs.timestamp
                }
            elif vital_signs.heartBeat > 102 or vital_signs.heartBeat < 58:
                alert = {
                    'type': 'vital_signs_alert',
                    'alert': 'Abnormal heart beat',
                    'value': vital_signs.heartBeat,
                    'isRead': False,
                    'userId': str(client['_id']),
                    'firstName': client['firstName'],
                    'lastName': client['lastName'],
                    'timestamp': vital_signs.timestamp
                }
            
            if alert:
                try:
                    await alerts_collection.insert_one(alert)
                except Exception as e:
                    print(f"Error inserting alert: {e}")
                    continue

            print(f"Received data: {message}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    except WebSocketDisconnect:
        print("WebSocket connection closed")
