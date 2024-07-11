import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

# base connection
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = PropanApp(broker)

# declare as schenge
exchange = RabbitExchange("topic-exchange", type=ExchangeType.TOPIC)

# queues
queue_1 = RabbitQueue("test-queue-1", routing_key="*.info")
queue_2 = RabbitQueue("test-queue-2", routing_key="*.debug")
queue_3 = RabbitQueue("test-queue-2", routing_key="logs.*")

# listen a q1
@broker.handle(queue_1, exchange)
async def handler1():
	print("handler1")

# listen a q2
@broker.handle(queue_2, exchange)
async def handler2():
	print("handler2")

# listen a q3
@broker.handle(queue_2, exchange)
async def handler2():
	print("handler3")

# simulation activities
@app.after_startup
async def send_messages():
	
    # send messages with patterns .derbug and .info
	await broker.publish(routing_key="logs.info", exchange=exchange)
	await broker.publish(routing_key="logs.debug", exchange=exchange)


if __name__ == "__main__":
    asyncio.run(app.run())