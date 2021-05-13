from flask import Flask, jsonify, render_template, Response
from flask import Blueprint
from flask import request
from pykafka import KafkaClient
import os,json,sys
import time,math,random
"""Example Kafka consumer."""
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
LEGIT_TOPIC = os.environ.get('LEGIT_TOPIC')
FRAUD_TOPIC = os.environ.get('FRAUD_TOPIC')

def get_kafka_client():
    kafkabrokerup=True
    while kafkabrokerup:
        try:
            kafka_client=KafkaClient(hosts=KAFKA_BROKER_URL)
            kafkabrokerup=False
        except:
            kafkabrokerup=True
    return kafka_client


detector_api = Blueprint('detector_api', __name__)

def is_suspicious(transaction: dict) -> bool:
    """Determine whether a transaction is suspicious."""
    return transaction['amount'] >= 900

@detector_api.route('/consumer/<type>', methods=['GET'])
def detector():
    try:
        client = get_kafka_client()
        legit_topic = client.topics[LEGIT_TOPIC]
        legit_producer = legit_topic.get_sync_producer()
        fraud_topic = client.topics[FRAUD_TOPIC]
        fraud_producer = fraud_topic.get_sync_producer()
        # consumer=client.topics[TRANSACTIONS_TOPIC].get_simple_consumer()
        print("abcd")
        def events():
            for i in client.topics[TRANSACTIONS_TOPIC].get_simple_consumer():
                # yield 'data:{0}\n\n'.format(i.value.decode())
                transaction = json.loads(i.value.decode())
                if transaction["type"]==type:
                    if is_suspicious(transaction):
                        fraud_producer.produce(i.value)
                        yield FRAUD_TOPIC+':{0}\n\n'.format(i.value.decode())
                else:
                    legit_producer.produce(i.value)
                    yield LEGIT_TOPIC+':{0}\n\n'.format(i.value.decode())
        return Response(events(), mimetype="text/event-stream")
    except Exception as e:
        return({"statusCode": 400,"error_message": str(e)})         