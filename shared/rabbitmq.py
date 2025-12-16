import os
import json
import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

class RabbitMQManager:
    def __init__(self):
        self.connection = None
        self.channel = None
    
    async def connect(self):
        """Establish connection to RabbitMQ"""
        self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()
        return self.channel
    
    async def close(self):
        """Close connection"""
        if self.connection:
            await self.connection.close()
    
    async def declare_exchange(self, exchange_name: str, exchange_type: str = "fanout"):
        """Declare an exchange"""
        return await self.channel.declare_exchange(
            exchange_name, 
            exchange_type,
            durable=True
        )
    
    async def declare_queue(self, queue_name: str, durable: bool = True):
        """Declare a queue"""
        return await self.channel.declare_queue(
            queue_name,
            durable=durable
        )
    
    async def publish_message(self, exchange_name: str, routing_key: str, message: dict):
        """Publish message to exchange"""
        if not self.channel:
            await self.connect()
        
        exchange = await self.declare_exchange(exchange_name)
        message_body = json.dumps(message).encode()
        
        await exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key
        )
    
    async def consume_messages(self, queue_name: str, callback):
        """Consume messages from queue"""
        if not self.channel:
            await self.connect()
        
        queue = await self.declare_queue(queue_name)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        message_body = json.loads(message.body.decode())
                        await callback(message_body)
                    except Exception as e:
                        print(f"Error processing message: {e}")

# Global instance
rabbitmq_manager = RabbitMQManager()

# Event definitions
class EventTypes:
    GUEST_CHECKED_IN = "guest.checked_in"
    GUEST_CHECKED_OUT = "guest.checked_out"
    ORDER_CREATED = "order.created"
    ORDER_UPDATED = "order.updated"
    AMENITY_REQUESTED = "amenity.requested"
    AMENITY_COMPLETED = "amenity.completed"
    TABLE_RESERVED = "table.reserved"
    PAYMENT_PROCESSED = "payment.processed"