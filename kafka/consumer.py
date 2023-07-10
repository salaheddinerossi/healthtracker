from confluent_kafka import Consumer, KafkaError, Producer
from pymongo import MongoClient
import json

# Define the Kafka configuration
consumer_conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'group1', 'auto.offset.reset': 'earliest'}
producer_conf = {'bootstrap.servers': 'localhost:9092'}

# Create a Consumer instance with the configuration
consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

# Subscribe to the 'vitalSigns' topic
consumer.subscribe(['vitalSigns'])

# Create a MongoDB client
client = MongoClient('mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/')

# Access the 'vitalSigns' collection in the 'health' database
db = client['HealthTracking']
vital_signs_collection = db['vitalSigns']
alerts_collection = db['Alerts']

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    # Parse message
    message = json.loads(msg.value().decode('utf-8'))

    # Insert the message into the MongoDB collection
    print(message)
    vital_signs_collection.insert_one(message)

    # Generate and send alert if vital signs are abnormal
    alert = None
    if message['bodyTemperature'] > 37.59:
        alert = {'type': 'vital_signs_alert', 'alert': 'High temperature', 'value': message['bodyTemperature'], 'isRead': False}
    elif message['bloodPressure'] > 121 or message['bloodPressure'] <78:
        alert = {'type': 'vital_signs_alert', 'alert': 'Abnormal blood pressure', 'value': message['bloodPressure'], 'isRead': False}
    elif message['heartBeat'] > 102 or message['heartBeat'] < 58:
        alert = {'type': 'vital_signs_alert', 'alert': 'Abnormal heart beat', 'value': message['heartBeat'], 'isRead': False}

    if alert:
        # Include the client's _id, firstName and lastName in the alert
        alert['userId'] = message['userId']
        alert['firstName'] = message['firstName']
        alert['lastName'] = message['lastName']

        # Send alert to 'alerts_topic' in Kafka
        producer.produce('alerts_topic', value=json.dumps(alert))
        producer.flush()

        # Add a timestamp to the alert and store it in MongoDB
        alert['timestamp'] = message['timestamp'] # use the timestamp from the message
        alerts_collection.insert_one(alert)
        print(alert)


consumer.close()
