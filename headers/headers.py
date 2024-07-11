import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

# base connection
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = PropanApp(broker)

# headers 
exch = RabbitExchange("headers_exchange", type=ExchangeType.HEADERS)

# declare queue with headers key 1
queue_1 = RabbitQueue(
	"test-queue-1",
	bind_arguments={ "key": 1 }
)

# declare queueu with heades key 2 key2 2
queue_2 = RabbitQueue(
	"test-queue-2",
	bind_arguments={
		"key": 2, "key2": 2,
		"x-match": "any"
	}
)

# declare queue with key2 2
queue_3 = RabbitQueue(
	"test-queue-3",
	bind_arguments={
		"key": 2, "key2": 2,
		"x-match": "all"
	}
)

# listen a queue 1
@broker.handle(queue_1, exch)
async def handler1():
	print("handler1")

# listen quuue 2
@broker.handle(queue_2, exch)
async def handler2():
	print("handler2")

# listen queue3
@broker.handle(queue_3, exch)
async def handler3():
	print("handler3")

# simulation a activities
@app.after_startup
async def send_messages():
	# send messages with headers key 1
	await broker.publish(exchange=exch, headers={ "key": 1 })
	
	# send message with headerrs with key 2 
	await broker.publish(exchange=exch, headers={ "key": 2 })
	
    # send message with header with key2 2 
	await broker.publish(exchange=exch, headers={ "key2": 2 })
	
    # send message with headers key1 2, key2 2 
	await broker.publish(exchange=exch, headers={
		"key": 2, "key2": 2
	})

if __name__ == "__main__":
    asyncio.run(app.run())