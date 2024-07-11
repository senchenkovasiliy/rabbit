import asyncio
import aio_pika

RABBIT_REPLY = "amq.rabbitmq.reply-to"

async def main():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )

    async with connection:
        channel = await connection.channel()

        callback_queue = await channel.get_queue(RABBIT_REPLY)

        # create a queue for answer
        rq = asyncio.Queue(maxsize=1)

        # subscribe
        consumer_tag = await callback_queue.consume(
            callback=rq.put,  # put message asyncio.Queue
            no_ack=True,  # flag to turn in True
        )

        # publish
        await channel.default_exchange.publish(
            message=aio_pika.Message(
                body=b"hello",
                reply_to=RABBIT_REPLY  # direction a queue for answer
            ),
            routing_key="test"
        )

        # get answer asyncio.Queue
        response = await rq.get()
        print(response.body)

        # cleanresourses in  RABBIT_REPLY
        await callback_queue.cancel(consumer_tag)

asyncio.run(main())