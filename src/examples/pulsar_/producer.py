import asyncio
import pulsar
import time
import datetime
import json

async def produce_transactions():
    """
    Produce transactions sets up a proudcer that creates transactions.
    It is necessary to have exactly once semantics. Additionally, logs
    will be produced with several brokers at once
    """
    from examples import get_settings, get_logger

    settings = get_settings()

    client = pulsar.Client(settings.pulsar_service_url)
    producer = client.create_producer(settings.create_topic("sensor-events"))

    while True:
        event = {
            "device_id": "sensor-123",
            "temperature": round(20 + 5 * (0.5 - time.time() % 1), 2),
            "timestamp": datetime.datetime.now(tz=datetime.UTC).isoformat()
        }
        producer.send(json.dumps(event).encode('utf-8'))
        get_logger(__name__).info(f"Sent: {event}")
        await asyncio.sleep(0.1)
