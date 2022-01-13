

class CommandHandler():
    async def handle_command(self, message):
        await message.channel.send("command detected")
