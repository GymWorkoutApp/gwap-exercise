import pickle

from gwa_framework.schemas.pub_sub import PubSubMessage
from kafka import KafkaProducer

from src.settings import GWA_ENVIRONMENT
from src.settings import GWA_KEY
from src.settings import PubSubSettings


def get_producer() -> KafkaProducer:
    return KafkaProducer(bootstrap_servers=f'{PubSubSettings.HOST}:{PubSubSettings.PORT}',
                         client_id=f'{GWA_ENVIRONMENT}-{GWA_KEY}',
                         max_block_ms=6000,
                         value_serializer=lambda m: pickle.dumps(m),
                         key_serializer=lambda m: pickle.dumps(m),
                         api_version=(0, 10))


def send_message(topic_name, value: PubSubMessage = None, key: str = None):
    if value is None:
        raise Exception('Value is required.')

    value_primitive = value.to_primitive()

    if not key:
        key = hash(value)

    try:
        get_producer().send(topic_name, key=key, value=value_primitive)
        get_producer().flush()
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))
        raise ex
