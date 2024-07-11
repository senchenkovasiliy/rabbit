import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

# base connection
broker = RabbitBroker('amqp://guest:guest@localhost:5672/')
app = PropanApp(broker=broker)

# set exchange direct
exchange = RabbitExchange('direct-exchenge', type=ExchangeType.DIRECT)

# net of queues 
queue_first = RabbitQueue('my-test-quque-first')
queue_second = RabbitQueue('my-test-ququq-second')

# listen queue first
@broker.handle(queue_first, exchange=exchange)
async def handler_first():
    print('my handler first')

# listen queue second
@broker.handle(queue_second, exchange=exchange)
async def handler_second():
    print('my handle secodn')

# simulation messages from another services
@app.after_startup
async def send_messages():
    """Sending messaged in exchanes in queues"""

    # first
    await broker.publish(exchange=exchange, routing_key='my-test-queue-first')
    # second
    await broker.publish(exchange=exchange, routing_key='my-test-queue-second')

if __name__ == '__main__':
    asyncio.run(app.run())