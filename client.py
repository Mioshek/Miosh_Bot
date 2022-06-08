import discord
import LinuxConsole
import time
import config

class MyClient(discord.Client):
    data = config.path_setter()
    
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print("ping = ""%.1f" %(super().latency*1000), "ms")
        
        
        

class EventReceiver(MyClient):
    
    async def on_message(self, message):
        # print('Message from {0.author}: {0.content}'.format(message))
        
        if message.content.startswith("$"):
            await message.channel.send(LinuxConsole.Console.execute_command(message,MyClient.data))
        if message.content.startswith("%ping"): 
            await ping(message)  
        if message.content.startswith("%gigachad"): await gigachad(message) 
    
    # async def on_message_delete

client = MyClient()
events = EventReceiver()

async def ping(message):
   before = time.monotonic()
   try:await message.delete()
   except: pass
   ping = ((time.monotonic() - before) * 1000)-60
   await message.channel.send(f"Ping: `{int(ping)}ms`")
   
async def gigachad(message):
    await message.channel.send("https://tenor.com/view/gigachad-chad-gif-20773266")
   

events.run(MyClient.data["token"])