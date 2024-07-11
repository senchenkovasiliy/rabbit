import asyncio
from functools import partial
import aio_pika


# create conbsumer
async def consumer(
    msg: aio_pika.IncomingMessage,
    channel: aio_pika.RobustChannel
):
    async with msg.process():
        print(msg.body)

        # must be a answers?
        if msg.reply_to:
            # send answer in exchange
            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=b"hello!",
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,  
            )


async def main():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )

    queue_name = "test"

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)
        # movie a channel acros partial
        await queue.consume(partial(consumer, channel=channel))

        try:
            await asyncio.Future()
        except Exception:
            pass

asyncio.run(main())