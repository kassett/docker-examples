import asyncio
from functools import lru_cache

import click
from pydantic_settings import BaseSettings
from urllib.parse import urlparse
import clickhouse_connect


class Config(BaseSettings):
    pulsar_service_url: str = "pulsar://localhost:6650"
    pulsar_transaction_topic: str = "persistent://public/default/transactions"
    pulsar_campaign_details_topic: str = "persistent://public/default/campaign-details"

    clickhouse_url: str = "clickhouse://examples:examples@localhost:8123/examples"

    def get_clickhouse_client(self):
        parsed = urlparse(self.clickhouse_url)

        if parsed.scheme != "clickhouse":
            raise ValueError(f"Invalid scheme '{parsed.scheme}' in clickhouse_url. Expected 'clickhouse://'")

        username = parsed.username or "default"
        password = parsed.password or ""
        host = parsed.hostname or "localhost"
        port = parsed.port or 8123
        database = parsed.path.lstrip("/") if parsed.path else "default"

        return clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
        )

@lru_cache
def get_settings() -> Config:
    return Config()


@click.group
def cli():
    pass

@cli.group("pulsar")
def pulsar_group():
    pass


@pulsar_group.command("produce-transactions")
def pulsar_produce_transactions_command():
    from examples.pulsar_ import producer

    asyncio.run(producer.produce_transactions())


@pulsar_group.command("consume-transactions")
def pulsar_consume_transactions_command():
    from examples.pulsar_ import consumer

    asyncio.run(consumer.consume_transactions())

@pulsar_group.command("consume-campaign-details")
def pulsar_consume_campaign_details_command():
    from examples.pulsar_ import consumer

    asyncio.run(consumer.consume_campaign_details())


if __name__ == "__main__":
    cli()