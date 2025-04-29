import asyncio
from functools import lru_cache

import click
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    pulsar_service_url: str = "pulsar://localhost:6650"

    def create_topic(self, topic: str) -> str:
        return f"persistent://public/default/{topic}"


@lru_cache
def get_settings() -> Config:
    return Config()


@click.group
def cli():
    pass


@cli.command("pulsar-demo")
def pulsar_demo_command():
    from examples.pulsar_ import producer, consumer

    asyncio.run(consumer.exclusive_subscription())


if __name__ == "__main__":
    cli()