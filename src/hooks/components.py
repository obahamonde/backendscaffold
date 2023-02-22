"""Single purpose decorators for hooks."""


import asyncio


from typing import Any, Callable, Optional, List, Coroutine


from enum import Enum


from functools import wraps


from aio_pika import connect_robust, Message


from aioredis import Redis


from httpx import AsyncClient


from src.config import env

from src.hooks.helpers import b64_encode, b64_decode


# pylint: disable=dangerous-default-value
# pylint: disable=line-too-long


class Cache:

    """Caching entity for storing frequently used data."""

    def __init__(self):
        self.redis = Redis(
            host=env.REDIS_HOST,
            port=env.REDIS_PORT,
            password=env.REDIS_PASSWORD,
            decode_responses=True,
            encoding="utf-8",
        )

    async def get(self, key: str) -> Optional[bytes]:
        """Get a value from the cache."""

        return await self.redis.get(key)

    async def set(self, key: str, value: bytes, expire: int = 0) -> None:
        """Set a value in the cache."""

        await self.redis.set(key, value, expire)

    async def delete(self, key: str) -> None:
        """Delete a value from the cache."""

        await self.redis.delete(key)

    def __call__(self, _function: Callable, ttl: int = 0):
        """Decorator for caching."""

        @wraps(_function)
        async def wrapper(*args, **kwargs):
            """Wrapper for caching."""

            key = b64_encode(f"{_function.__name__}:{args}:{kwargs}")

            value = await self.get(key)

            if value is None:
                value = await _function(*args, **kwargs)

                await self.set(key, value, ttl)

            return value

        return wrapper


class ExchangeType(Enum):

    """Enum for exchange types."""

    DIRECT = "direct"

    FANOUT = "fanout"

    TOPIC = "topic"

    HEADERS = "headers"


class Queue:

    """Class that represents the RabbitMQ stack and encapsulates the logic for all its components."""

    async def connect(self, qos: int = 10):
        """Connect to the RabbitMQ server."""

        self.connection = await connect_robust(url=env.AMQP_URL)

        async with self.connection:
            self.channel = await self.connection.channel()

            await self.channel.set_qos(prefetch_count=qos)

    async def exchange(self, name: str, exchange_type: ExchangeType):
        """Create an exchange."""

        async with self.connection:
            return await self.channel.declare_exchange(name, exchange_type.value)

    async def queue(self, name: str, routing_key: str, exchange: str):
        """Create a queue."""

        async with self.connection:
            queue = await self.channel.declare_queue(name)

            await queue.bind(exchange, routing_key)

            return queue

    async def publish(self, routing_key: str, message: str):
        """Publish a message to the exchange."""

        async with self.connection:
            await self.channel.default_exchange.publish(
                Message(body=message.encode()), routing_key=routing_key
            )

    async def consume(self, queue: str, callback: Callable):
        """Consume messages from the queue."""

        async with self.connection:
            _queue = await self.channel.declare_queue(queue)

            async with _queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        await callback(message)

                        yield message

    def consumer(self, queue: str, callback: Callable):
        """Decorator for consuming messages from a queue."""

        def decorator(function_: Callable):
            @wraps(function_)
            async def wrapper(*args, **kwargs):
                """Wrapper for consuming messages from a queue."""

                async with self.connection:
                    _queue = await self.channel.declare_queue(queue)

                    async with _queue.iterator() as queue_iter:
                        async for message in queue_iter:
                            async with message.process():
                                await callback(message)

                                await function_(message, *args, **kwargs)

            return wrapper

        return decorator

    def producer(self, routing_key: str):
        """Decorator for publishing messages to the exchange."""

        def decorator(function_: Callable):
            @wraps(function_)
            async def wrapper(*args, **kwargs):
                """Wrapper for publishing messages to the exchange."""

                async with self.connection:
                    await self.channel.default_exchange.publish(
                        Message(body=await function_(*args, **kwargs).encode()),
                        routing_key=routing_key,
                    )

            return wrapper

        return decorator


default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Content-Type": "application/json",
}


class Http:

    """Class that represents the HTTP stack and encapsulates the logic for all its components."""

    async def get(self, url: str, headers: dict = default_headers) -> Optional[dict]:
        """Send a GET request."""

        async with AsyncClient() as client:
            response = await client.get(url, headers=headers)

            return response.json()

    async def post(
        self, url: str, data: dict, headers: dict = default_headers
    ) -> Optional[dict]:
        """Send a POST request."""

        async with AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)

            return response.json()

    async def put(
        self, url: str, data: dict, headers: dict = default_headers
    ) -> Optional[dict]:
        """Send a PUT request."""

        async with AsyncClient() as client:
            response = await client.put(url, data=data, headers=headers)

            return response.json()

    async def delete(self, url: str, headers: dict = default_headers) -> Optional[dict]:
        """Send a DELETE request."""

        async with AsyncClient() as client:
            response = await client.delete(url, headers=headers)

            return response.json()

    async def patch(
        self, url: str, data: dict, headers: dict = default_headers
    ) -> Optional[dict]:
        """Send a PATCH request."""

        async with AsyncClient() as client:
            response = await client.patch(url, data=data, headers=headers)

            return response.json()

    async def text(self, url: str, headers: dict = default_headers) -> Optional[str]:
        """Send a GET request and return the response text."""

        async with AsyncClient() as client:
            response = await client.get(url, headers=headers)

            return response.text

    async def blob(self, url: str, headers: dict = default_headers) -> Optional[bytes]:
        """Send a GET request and return the response blob."""

        async with AsyncClient() as client:
            response = await client.get(url, headers=headers)

            return response.content

    async def fetch(
        self, urls: List[str], headers: dict = default_headers
    ) -> List[Optional[dict]]:
        """Perform multiple JSON requests concurrently."""

        return await asyncio.gather(*[self.get(url, headers=headers) for url in urls])

    async def scrape(
        self, urls: List[str], headers: dict = default_headers
    ) -> List[Optional[str]]:
        """Perform multiple text requests concurrently."""

        return await asyncio.gather(*[self.text(url, headers=headers) for url in urls])

    async def batch(
        self, urls: List[str], headers: dict = default_headers
    ) -> List[Optional[bytes]]:
        """Perform multiple blob requests concurrently."""

        return await asyncio.gather(*[self.blob(url, headers=headers) for url in urls])
