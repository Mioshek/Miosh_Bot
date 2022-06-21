import LinuxConsole
import config
import bot_commands
from discord.ext import commands

data = config.default_path_setter()#sets default path and returns loaded json data
bot_prefix = data["bot_prefix"]
bot = commands.Bot(command_prefix=bot_prefix)    


class MyClient():
    changed_prefix = ""
    @bot.event
    async def on_ready():
        print('Logged on as {0}!'.format(bot.user))
        print("ping = ""%.1f" %(bot.latency*1000), "ms")
    
    @bot.event
    async def on_message(ctx):
        print('Message from {0.author}: {0.content}'.format(ctx))
        config.create_log(ctx)
        cmd = bot_commands.AllCommands(data, ctx, bot)
        second_arg = await cmd.execute_bot_command()
        if second_arg is not None and len(second_arg) == 1:
            MyClient.changed_prefix = second_arg
    
    @bot.event
    async def on_reaction_add(reaction, user):
        print("here")
        if user != bot.user:
            await bot_commands.AdminCommands.change_prefix_in_json(data, reaction, MyClient.changed_prefix)

client = MyClient()

@staticmethod
def run():    
    bot.run(data["token"])

