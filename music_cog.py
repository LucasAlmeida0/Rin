import discord
from discord.ext import commands
import youtube_dl


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.songs = []

    @commands.command(name='join', help='Bot joins in your voice channel')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return
        voice_client = ctx.voice_client
        voice_channel = ctx.author.voice.channel
        if voice_client is None:
            await voice_channel.connect()
            await ctx.send(f"Joined {voice_channel}")
        else:
            if voice_client.is_connected():
                await voice_client.move_to(voice_channel)
                await ctx.send(f"Moved to{voice_channel}")
            else:
                await voice_client.connect()
                await ctx.send(f"Joined {voice_channel}")

    # Leaves a voice channel and stop the queue

    @commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name="play", description="Play a music from the given link")
    async def play(self, ctx, *, url):
        print("play command called")
        async with ctx.typing():
            voice_client = ctx.voice_client
            if not self.songs:
                if voice_client is None:
                    await self.join(ctx)
                    voice_client = ctx.voice_client
                if not voice_client.is_playing():
                    await MusicCog.play_song(ctx, url)
                else:
                    self.songs.append(url)
                    await ctx.send(f'{url} added to the playlist')
            else:
                self.songs.append(url)
                await ctx.send(f'{url} added to the playlist')

    @staticmethod
    async def play_song(ctx, url):
        voice_client = ctx.voice_client
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'default_search': 'auto',
            'verbose': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            url = info['formats'][0]['url']
            source = discord.FFmpegPCMAudio(url, executable="ffmpeg")
            voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'Now playing: {title}')
