import discord
from discord.ext import commands

class VoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', aliases=['j','J','Join'])
    async def join(self, ctx, external=False):
    # external: True if called from somewhere outside of this class

        # Is the user in a channel, and is the bot already in a channel?
        if (ctx.author.voice):

            if ctx.voice_client == None:
                voice_channel = ctx.message.author.voice.channel
                await voice_channel.connect()
                if not external: await ctx.message.add_reaction("✅")
            else:
                if not external: await ctx.message.add_reaction("❌")
                if not external: await ctx.send("I'm already in a voice channel")

        else:
            if not external: await ctx.message.add_reaction("❌")
            await ctx.send("You must be in a voice channel for me to join")

        return ctx.voice_client
   
    @commands.command(name='leave', aliases=['l','L','Leave'])
    async def leave(self, ctx):

        if ctx.voice_client:
            await ctx.message.add_reaction("✅")
            await ctx.voice_client.disconnect()
        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("I am not in a voice channel")


async def setup(bot):
    await bot.add_cog(VoiceChannels(bot))

# A little tomfoolery
if __name__ == '__main__':
    print("Wrong file bozo")