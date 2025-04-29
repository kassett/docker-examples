import pulsar


async def consume_transactions():
    """
    Consume transactions one at a time.
    """
    from examples import get_logger, get_settings

    pulsar.SubscriptionNotFound
    settings = get_settings()
    logger = get_logger(__name__)

    client = pulsar.Client(settings.pulsar_service_url)
    consumer = client.subscribe(
        settings.create_topic("sensor-events"),
        subscription_name='exclusive-log-subscription',
        subscription_type=pulsar.SubscriptionType.Exclusive
    )

    try:
        while True:
            msg = consumer.receive()
            try:
                logger.info(f"Exclusive Consumer Received: {msg.data().decode('utf-8')}")
                consumer.acknowledge(msg)
            except Exception as e:
                consumer.negative_acknowledge(msg)
                logger.error(f"Failed to process message: {e}")
    finally:
        client.close()



async def consume_transaction_logs():
    """
    Consume logs for transactions one at a time.
    """
    from examples import get_logger, get_settings

    pulsar.SubscriptionNotFound
    settings = get_settings()
    logger = get_logger(__name__)

    client = pulsar.Client(settings.pulsar_service_url)
    consumer = client.subscribe(
        settings.create_topic("sensor-events"),
        subscription_name='exclusive-log-subscription',
        subscription_type=pulsar.SubscriptionType.Exclusive
    )

    try:
        while True:
            msg = consumer.receive()
            try:
                logger.info(f"Exclusive Consumer Received: {msg.data().decode('utf-8')}")
                consumer.acknowledge(msg)
            except Exception as e:
                consumer.negative_acknowledge(msg)
                logger.error(f"Failed to process message: {e}")
    finally:
        client.close()