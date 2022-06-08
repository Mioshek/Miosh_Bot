import discord

class DisplayHelp():
    
    def __init__(self,client,message) -> None:
        self.my_id = '<@489788192145539072>'
        self.help_text = "Hi I'm Miosh-Bot and my current prefix is: {prefix} \n Available commands are: \n {prefix}changeprefix or cp \n {prefix}join or j \n {prefix}leave or l \n If you had any problems contact me {my_id}"
        self.message = message
        self.client = client
    
    async def print_help(self):
        if self.message.author == self.client.user: return
        if self.message.content.startswith(self.prefix+'help') or self.message.content.startswith(self.prefix+'h'):
            await self.message.channel.send(self.help_text.format(prefix=self.prefix, my_id =self.my_id))