class MessageHandler():
    async def handle_message(self, message):
        await message.channel.send("general messages detected")
