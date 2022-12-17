import json
import asyncio

import aioredis

class Chat:
    def __init__(self, room_name):
        self.room_name = room_name

    async def start_db(self):
        self.redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
        await self.redis.set("room_name", self.room_name)

    async def save_message(self, message_dictionary):
        room_name = await self.redis.get("room_name")
        message_json = json.dumps(message_dictionary)
        await self.redis.rpush(room_name, message_json)

    async def clear_db(self):
        await self.redis.flushall()

    async def get_all_messages(self):
        room_name = await self.redis.get("room_name")
        message_jsons = await self.redis.lrange(room_name, 0, -1)
        messages = []
        for message in message_jsons:
            message_dictionary = json.loads(message)
            messages.append(message_dictionary)
        return messages

    async def get_name(self):
        return await self.redis.get("room_name")


async def main():
    chat_db = Chat("messages")
    await chat_db.start_db()
    await chat_db.save_message({"handle": "first_user", "message": "hey"})
    await chat_db.save_message({"handle": "first_user", "message": "hey"})
    await chat_db.save_message({"handle": "second_user", "message": "What's up?"})
    await chat_db.save_message({"handle": "first_user", "message": "all good!"})

    chat_messages = await chat_db.get_all_messages()
    chat_db_name = await chat_db.get_name()
    print(f" {chat_db_name} ")
    for message in chat_messages:
        print(f'  {message["handle"]} | {message["message"]} ')
    await chat_db.clear_db()

asyncio.run(main())