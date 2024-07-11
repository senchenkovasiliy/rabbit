import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

# base connection
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = PropanApp(broker)

# Fanout Exchange
exchange = RabbitExchange("fonout-exchange", type=ExchangeType.FANOUT)

# queueus
queue_fists = RabbitQueue("my-test-queue-1")
queue_second = RabbitQueue("my-test-queue-1")

# listen queue
@broker.handle(queue_fists, exchange)
async def handle_first():
	print("handler1")

# listen queue
@broker.handle(queue_second, exchange)
async def handler_second():
	print("handler2")

# activities simulation
@app.after_startup
async def send_messages():
	await broker.publish(exchange=exchange)

if __name__ == "__main__":
    asyncio.run(app.run())