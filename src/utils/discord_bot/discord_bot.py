import discord

class DiscordBot(discord.Client):
    def __init__(self, intents, guild_id, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.guild_id = guild_id
    
    def set_message(self, embed):
        self.embed = embed
    
    def set_channel(self, channel):
        self.channel = channel

        
    async def on_ready(self):
        guild = self.get_guild(int(self.guild_id))
        channel = discord.utils.get(guild.text_channels, name=self.channel)

        if channel is None:
            channel = await guild.create_text_channel(self.channel)
        
        await channel.send(embed=self.embed)
        await self.close()
