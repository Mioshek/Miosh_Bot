import LinuxConsole
import time
import discord
from Utilities import Utilities
import data_manager
from random import randint

class AllCommands:
    def __init__(self, data, ctx, bot) -> None:
        self.data = data
        self.ctx = ctx
        self.bot = bot
        self.bot_prefix = data["bot_prefix"]
        self.linux_prefix = data["linux_prefix"]
        self.admin_ids = data["admin_ids"]
        self.raw_data = Utilities.split_into_parts(ctx.content[1:], " ", False)
    
    async def execute_bot_command(self):
        if self.ctx.author.id in self.admin_ids.values():
            if self.ctx.content.startswith(self.linux_prefix):
                await AdminCommands.linux_commands(self.ctx, self.data)
            if self.raw_data[0] == "mkadm":
                await AdminCommands.add_admin(self.ctx, self.data, self.raw_data, self.bot)
            if self.raw_data[0] == "rmadm":
                await AdminCommands.rm_admin(self.ctx, self.data, self.raw_data, self.bot)      
        
        if self.ctx.content.startswith(self.bot_prefix + "ping"): 
            await NormalCommands.ping(self.ctx) 
        if self.ctx.content.startswith(self.bot_prefix + "gigachad"):
            await NormalCommands.gigachad(self.ctx)
        if self.ctx.content.startswith(self.bot_prefix + "roll dice"):
            await NormalCommands.roll_dice(self.ctx)
    

class AdminCommands:
    
    async def linux_commands(ctx, data):
        await ctx.channel.send(LinuxConsole.Console.determine_command(ctx,data))
        
    async def add_admin(ctx, data, raw_data, bot):
        raw_new_admin = raw_data[1]
        new_admin = int(raw_new_admin[2:-1])
        admin_username = await bot.fetch_user(new_admin)
        await ctx.channel.send(f"{admin_username} was added to Admin Users List")
        admins = data["admin_ids"]
        admins[str(admin_username)] = new_admin
        data_manager.JsonManager.write_to_json(data)
        
    async def rm_admin(ctx, data, raw_data, bot):
        raw_new_admin = raw_data[1]
        new_admin = int(raw_new_admin[2:-1])
        admin_username = await bot.fetch_user(new_admin)
        await ctx.channel.send(f"{admin_username} was deleted from Admin Users List")
        admins = data["admin_ids"]
        admins.pop(str(admin_username))
        data_manager.JsonManager.write_to_json(data)
    
    async def change_prefix():
        pass
    

class NormalCommands():

    async def ping(ctx):
        before = time.perf_counter_ns()
        try:await ctx.delete()
        except: pass
        ping:float = ((time.perf_counter_ns() - before)/1_000_000)
        ping_field:str = f"{ping:.1f} ms"
        embed=discord.Embed(color=0x00ff00)
        embed.add_field(name="Ping: ", value=ping_field, inline=False)
        await ctx.channel.send(embed=embed)
     
    async def gigachad(ctx):
        await ctx.channel.send("https://tenor.com/view/gigachad-chad-gif-20773266")
        
    async def roll_dice(ctx):
        path:str = data_manager.PATH + "/" + "dice" + "/"
        dices:list = [path + "one_eye_dice.png",
        path + "two_eye_dice.png",
        path + "three_eye_dice.png",
        path + "four_eye_dice.png",
        path + "five_eye_dice.png",
        path + "six_eye_dice.png"]
        eye_count:int = randint(0,5)
        ready_dice_eyes:str = dices[eye_count]
        await ctx.channel.send(file=discord.File(ready_dice_eyes))

