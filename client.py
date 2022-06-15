import discord
import LinuxConsole
import time
import config
import data_manager
from discord.ext import commands

data = config.default_path_setter()#sets default path and returns loaded json data
bot_prefix = data["bot_prefix"]
linux_prefix = data["linux_prefix"]
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
        if ctx.content.startswith(linux_prefix):
            await ctx.channel.send(LinuxConsole.Console.determine_command(ctx, data))
        if ctx.content.startswith(bot_prefix + "ping"): 
            await ping(ctx)  
        if ctx.content.startswith(bot_prefix + "gigachad"): await gigachad(ctx) 
               
client = MyClient()

@staticmethod
def run():    
    bot.run(data["token"])

@bot.command()
async def ping(message):
    before = time.perf_counter_ns()
    try:await message.delete()
    except: pass
    ping:float = ((time.perf_counter_ns() - before)/1_000_000)
    ping_field:str = f"{ping:.1f} ms"
    embed=discord.Embed(color=0x00ff00)
    embed.add_field(name="Ping: ", value=ping_field, inline=False)
    await message.channel.send(embed=embed)
   
@bot.command()   
async def gigachad(message):
    await message.channel.send("https://tenor.com/view/gigachad-chad-gif-20773266")