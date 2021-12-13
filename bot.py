import discord
import time
import asyncio
import utils
import command_handler as ch
import message_handler as mh
# from discord.ext import commands

joined = 0
messages = 0
logDirPath = "logs/"
statsPath = "logs/stats.txt"
bannedPath = "logs/bannedMessages.txt"

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
    #
    # @commands.command(pass_context=True)
    async def on_message(self, message):
        global messages
        messages += 1
        serverId = self.get_guild(893683105909579786)
        channels = ["commands"] #restricting channels that can use commands
        bad_words = ["cai"]
        command_handler = ch.CommandHandler()
        message_handler = mh.MessageHandler()

        if str(message.channel) in channels:
            # don't respond to ourselves
            if message.author == self.user:
                return

            if message.content == '!users':
                await message.channel.send(f"""# of Members: {serverId.member_count}""")

            # if message.content.startswith('!'):
            #     command_handler.handle_message(message)

        for word in bad_words:
            if message.content.count(word) > 0:
                try:
                    record = 'Time: {}, Message: {}, Author: {} \n'.format(utils.format_gmtime(time.gmtime()), message.content, message.author)
                    with open(bannedPath, "a") as f:
                        f.write(record)
                    # await message.channel.purge(limit=1) needs permission
                    await message.channel.send('{}, please be careful of what you say!'.format(message.author.mention))
                except Exception as e:
                    print(e)

        # message_handler.handle_message(message)
        if message.content == 'private battle':
            await message.channel.send(file=utils.generate_private_battle(8)) # TODO get count input？

        if client.user.mentioned_in(message):
            await message.channel.send(message.author.display_name + " please don't speak to me without a mask!")

    async def on_member_join(self, member):
        global joined
        joined += 1
        await message.channel.send('Welcome to the Inkpolis! {}'.format(member.mention))


client = MyClient()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            record = 'Time: {}, Messages: {:0.0f}, Members Joined: {:0.0f} \n'.format(utils.format_gmtime(time.gmtime()), messages, joined)
            with open(statsPath, "a") as f:
                f.write(record)
                messages = 0
                joined = 0

                await asyncio.sleep(3600) # updates new msgs and users stats every 1 hour
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


client.loop.create_task(update_stats())
utils.get_resources();
client.run(utils.get_token());
