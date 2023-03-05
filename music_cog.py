import discord
from discord.ext import commands
from youtube_interaction import get_audio_stream, Song
import platform
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.p = Player(self.bot)

    @commands.command(name="play", aliases=['p','P','Play','PLAY', 'q', 'Q', 'Queue', 'queue', 'QUEUE'])
    async def play(self, ctx):

        if self.p.voice_client == None:
            await self.p.connect(ctx)

        # Process user's request
        message_content = ctx.message.content
        if " " in message_content:
            command, query = message_content.split(" ", 1)
        
        # Add generated song object to queue
        try:
            message = await ctx.send(f"Searching for \"{query}\"")
        except UnboundLocalError:
            await ctx.send("You can't search for nothing silly!")
        song = get_audio_stream(query)

        if song.success:
            await self.p.add_song(song)
            await message.edit(content=f"Added ***{song.title}*** to the queue")
            await ctx.message.add_reaction("✅")

            if not self.p.is_playing:
                await self.p.start_playing()
            else:
                await self.p.add_song(song)

        else:
            await message.edit(content=f"Failed to add song to queue")
            await ctx.message.add_reaction("❌")

class Player:
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.queue = []
        self.is_playing = False
        self.operating_system = platform.system()
        self.ffmpeg_options = {
            'options':'-vn',
            "before_options":"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }

    async def connect(self, ctx):
        join_command = self.bot.get_command('join')
        new_ctx = await self.bot.get_context(ctx.message, cls=type(ctx))
        self.voice_client = await new_ctx.invoke(join_command, external=True)

    async def add_song(self, song):
        self.queue.append(song)

    async def start_playing(self):

        while len(self.queue) != 0:
            song = self.queue.pop(0)
            self.is_playing = True

            if self.operating_system == "Windows":
                print(song.url)
                self.voice_client.play(discord.FFmpegPCMAudio(source=song.url, executable="C:/FFmpeg/ffmpeg.exe", options=self.ffmpeg_options))
            elif self.operating_system == "Linux":
                self.voice_client.play(discord.FFmpegPCMAudio(source=song.url, options=self.ffmpeg_options))


            while self.is_playing:
                await asyncio.sleep(.5)
        
        self.is_playing = False




# ================================

async def setup(bot):
    await bot.add_cog(Music(bot))

# A little tomfoolery
if __name__ == '__main__':
    print("Wrong file bozo")