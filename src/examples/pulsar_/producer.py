import asyncio
import pulsar
import datetime
import json
import random
import clickhouse_connect


async def produce_transactions():
    """
    Produce realistic transaction and campaign data with exactly-once semantics.
    Transactions are sent to an exactly-once topic and inserted into ClickHouse.
    Campaign metrics are sent to a multi-consumer topic and inserted into ClickHouse.
    """
    from examples import get_settings, get_logger
    from faker import Faker

    s = get_settings()
    log = get_logger(__name__)
    faker = Faker()

    # ClickHouse client
    ch_client = s.get_clickhouse_client()

    # Pulsar client
    client = pulsar.Client(s.pulsar_service_url, operation_timeout_seconds=30)

    transaction_producer = client.create_producer(
        topic=s.pulsar_transaction_topic,
        producer_name="txn-producer",
        send_timeout_millis=0,
        block_if_queue_full=True,
        batching_enabled=True
    )

    campaign_producer = client.create_producer(
        topic=s.pulsar_campaign_details_topic,
        producer_name="campaign-producer",
        send_timeout_millis=0,
        block_if_queue_full=True,
        batching_enabled=True
    )

    currencies = ["USD", "EUR", "GBP", "JPY", "AUD"]
    operating_systems = ["iOS", "Android", "Windows", "macOS", "Linux"]

    while True:
        try:
            now = datetime.datetime.now(tz=datetime.UTC)

            # Transaction
            from_account = faker.uuid4()
            to_account = faker.uuid4()
            currency = random.choice(currencies)
            amount = round(random.uniform(10, 1000), 2)

            transaction = {
                "from_account_id": from_account,
                "to_account_id": to_account,
                "currency": currency,
                "amount": amount,
                "timestamp": now.isoformat()
            }

            txn_json = json.dumps(transaction)
            transaction_producer.send(txn_json.encode('utf-8'))

            ch_client.insert(
                "sent_messages",
                data=[[s.pulsar_transaction_topic, txn_json, now.replace(tzinfo=None)]],
                column_names=["topic_name", "content", "timestamp"]
            )

            # Campaign
            campaign_event = {
                "campaign_id": faker.uuid4(),
                "country_code": faker.country_code(),
                "operating_system": random.choice(operating_systems),
                "impressions": random.randint(1000, 5000),
                "clicks": random.randint(50, 500),
                "conversions": random.randint(5, 50),
                "timestamp": now.isoformat()
            }

            campaign_json = json.dumps(campaign_event)
            campaign_producer.send(campaign_json.encode('utf-8'))

            ch_client.insert(
                "sent_messages",
                data=[[s.pulsar_campaign_details_topic, campaign_json, now.replace(tzinfo=None)]],
                column_names=["topic_name", "content", "timestamp"]
            )

            log.info(f"Sent TXN + wrote to ClickHouse: {transaction}")
            log.info(f"Sent Campaign + wrote to ClickHouse: {campaign_event}")

        except Exception as e:
            log.error(f"Error producing or writing to ClickHouse: {e}")

        await asyncio.sleep(0.5)