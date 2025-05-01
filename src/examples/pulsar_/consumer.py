import json
import pulsar
from pulsar import ConsumerType


async def consume_messages(topic, subscription_name, consumer_type, label):
    """
    Generic Pulsar message consumer.
    Logs and acknowledges messages from the specified topic.
    """
    from examples import get_settings, get_logger

    s = get_settings()
    log = get_logger(__name__)
    client = pulsar.Client(s.pulsar_service_url)

    consumer = client.subscribe(
        topic=topic,
        subscription_name=subscription_name,
        consumer_type=consumer_type,
        initial_position=pulsar.InitialPosition.Latest
    )

    while True:
        try:
            msg = consumer.receive(timeout_millis=5000)
            data = json.loads(msg.data())
            log.info(f"Processed {label}: {data}")
            consumer.acknowledge(msg)
        except pulsar.Timeout:
            continue
        except Exception as e:
            log.error(f"{label} error: {e}")
            consumer.negative_acknowledge(msg)

    client.close()


async def consume_transactions():
    from examples import get_settings, get_logger

    s = get_settings()
    await consume_messages(
        topic=s.pulsar_transaction_topic,
        subscription_name="txn-exactly-once-subscription",
        consumer_type=ConsumerType.Exclusive,
        label="Transaction"
    )


async def consume_campaign_details():
    from examples import get_settings, get_logger

    s = get_settings()
    await consume_messages(
        topic=s.pulsar_campaign_details_topic,
        subscription_name="campaign-metrics-shared-subscription",
        consumer_type=ConsumerType.Shared,
        label="Campaign"
    )
