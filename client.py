import LinuxConsole
import config
import bot_commands
from discord.ext import commands

data = config.default_path_setter()#sets default path and returns loaded json data
bot_prefix = data["bot_prefix"]
bot = commands.Bot(command_prefix=bot_prefix)    


class MyClient():
    
    @bot.event
    async def on_ready():
        print('Logged on as {0}!'.format(bot.user))
        print("ping = ""%.1f" %(bot.latency*1000), "ms")
    
    @bot.event
    async def on_message(ctx):
        print('Message from {0.author}: {0.content}'.format(ctx))
        config.create_log(ctx)
        cmd = bot_commands.AllCommands(data, ctx, bot)
        await cmd.execute_bot_command()
         
               
client = MyClient()

@staticmethod
def run():    
    bot.run(data["token"])

