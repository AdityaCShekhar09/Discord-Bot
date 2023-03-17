import discord
from discord.ext import commands
import random
from data import *
import datetime
import json
import platform
import cogs._json
import urllib
import asyncpraw
import requests
import os
import asyncio
from redvid import Downloader
from pytube import YouTube


reddit = Downloader()

def checkReddit(url, lengthReddit):
    reddit.url = url
    reddit.min = True
    reddit.log = False
    reddit.check()
    if reddit.duration > lengthReddit:
        return False
    else:
        return True


def renameReddit(name):
    dir = []
    for file in os.listdir():
        if file.endswith('.mp4'):
            dir.append(file)
    os.rename(dir[0], name)


def downloadReddit(url):
    reddit.max_s = 7.5 * (1 << 20)
    reddit.auto_max = True
    reddit.log = False
    reddit.url = url
    reddit.download()


def downloadYoutube(url):
    yt = YouTube(url)
    mp4files = yt.streams.filter(progressive=True, file_extension='mp4')
    yt.set_filename('savevideo.mp4')  
    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution) 
    try: 
        d_video.download("savevideo.mp4") 
    except: 
        pass


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = asyncpraw.Reddit(
            client_id="rB94t7N0zGcn1xMe_5TIow",
            client_secret="ZfJV31JT_tTftEBwgUMOE_z-iBMuIw",
            user_agent="Trickywacky")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has loaded")

    @commands.command(name="clear", help="Deletes messages")
    async def clear(self, ctx, *, amount):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        if amount == "all":
            await ctx.channel.purge(limit=20000)
        else:
            try:
                await ctx.channel.purge(limit=int(amount) + 1)
            except ValueError:
                await ctx.send("Something went wrong.")

    @commands.command(name="roast", help="Roasts someone")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def roast(self, ctx, *, name):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        await ctx.message.channel.send(f"{name} {random.choice(roast_quotes)}")

    @commands.command(name="ping", help="Returns bot ping")
    async def ping(self, ctx):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        await ctx.message.channel.send(f"{round(self.client.latency * 1000)}ms"
                                       )

    @commands.command(name="ask", help="Answers a question(yes or no)")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def ask(self, ctx, *, question):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        await ctx.send(random.choice(response))

    @commands.command(name="status", help="Shows bot info")
    async def stats(self, ctx):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)

        embed = discord.Embed(title=f'{self.client.user.name} Stats',
                              description='\uFEFF',
                              colour=random.choice(self.client.colors),
                              timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.client.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Bot Developer:', value="<@862374422749249556>")

        embed.set_footer(text=f"{self.client.user.name}")
        embed.set_author(name=self.client.user.name,
                         icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="send_dm", help="Sends a message to a member")
    async def send_dm(self, ctx, member: discord.Member, *, content):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        try:
            await member.send(content)
            await ctx.send(f':white_check_mark: Your Message has been sent')
        except:
            await ctx.send(':x: Member had their dm close, message not sent')

    @commands.command(name="snipe", help="Show recently deleted message")
    async def snipe(self, ctx):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        try:
            contents, author, channel_name, time = self.client.sniped_messages[
                ctx.guild.id]

        except:
            await ctx.channel.send("Couldn't find a message to snipe!")
            return

        embed = discord.Embed(description=contents,
                              color=random.choice(self.client.colors),
                              timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}",
                         icon_url=author.avatar_url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")

        await ctx.channel.send(embed=embed)

    @commands.command(name="meme", help="Sends a meme")
    async def meme(self, ctx):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        memeAPI = urllib.request.urlopen("http://meme-api.herokuapp.com/gimme")
        memeData = json.load(memeAPI)
        memeUrl = memeData['url']
        memeName = memeData['title']
        embed = discord.Embed(title=memeName,
                              color=random.choice(self.client.colors))
        embed.set_image(url=memeUrl)
        await ctx.send(embed=embed)

    @commands.command(name="video", help="Sends a reddit video")
    async def video(self, ctx, *link):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        await ctx.message.delete()
        for url in link:
          if "youtu" in url:
            try:
              downloadYoutube(url)
              async with ctx.typing():
                await ctx.send(
                            content=
                            f"YouTube video sent by {ctx.message.author.mention}",
                            file=discord.File(fp="savevideo.mp4"))
                os.remove("savevideo.mp4")
            except:
              pass
          
          elif "/comments/" in url:
            try:
                async with ctx.typing():
                    if checkReddit(url, 60):
                        downloadReddit(url)
                        renameReddit("savevideo.mp4")
                        await ctx.send(
                            content=
                            f"Reddit video sent by {ctx.message.author.mention}",
                            file=discord.File(fp="savevideo.mp4"))
                        os.remove("savevideo.mp4")
                        print(
                            f"\Reddit video sent by {ctx.message.author.mention}\n{url}\n{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+3))).time()}"
                        )
                      
                    else:
                        await ctx.send(
                            "Your video is longer than 60 seconds!\n(The reason behind this is the Discord upload limit.)",
                            delete_after=5.0)
                        await ctx.message.delete(delay=5)
                        print(
                            f"\nYour video is longer than 60 seconds!\n{url}\ndatetime.{datetime.now(datetime.timezone(datetime.timedelta(hours=+3))).time()}"
                        )
            except:
                await ctx.send("Something went wrong while getting the video.")
                print(
                    f"\nSomething went wrong while getting the video.\n{url}\n{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+3))).time()}"
                )
                os.remove("savevideo.mp4")
                asyncio.sleep(4)

    @commands.command(name="hot", help="Sends hot posts from reddit")
    async def hot(self, ctx, subreddit: str):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        sub = await self.reddit.subreddit(subreddit)
        count = 0
        async for submission in sub.hot(limit=100):
            url = submission.url
            if url.startswith("https://i.redd.it"):
                await ctx.send(submission.title)
                await ctx.send(submission.url)
                count = count + 1
            elif url.startswith("https://v.redd.it"):
                async with ctx.typing():
                    if checkReddit(url, 60):
                        try:
                            downloadReddit(url)
                            renameReddit("savevideo.mp4")
                            try:
                              await ctx.send(submission.title)
                              await ctx.send(file=discord.File(
                                fp="savevideo.mp4"))
                              count = count + 1
                              os.remove("savevideo.mp4")
                              asyncio.sleep(5)
                            except:
                              os.remove("savevideo.mp4")
                              ctx.channel.purge(limit=1)
                        except:
                            pass
            if count == 10:
                return

    @commands.command(nam="top", help="Sends top posts from subreddit")
    async def top(self, ctx, subreddit: str):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        sub = await self.reddit.subreddit(subreddit)
        count = 0
        async for submission in sub.top(limit=100):
            url = submission.url
            if url.startswith("https://i.redd.it"):
                await ctx.send(submission.title)
                await ctx.send(submission.url)
                count = count + 1
            elif url.startswith("https://v.redd.it"):
                async with ctx.typing():
                    if checkReddit(url, 60):
                        try:
                            downloadReddit(url)
                            renameReddit("savevideo.mp4")
                            try:
                              await ctx.send(submission.title)
                              await ctx.send(file=discord.File(
                                fp="savevideo.mp4"))
                              count = count + 1
                              os.remove("savevideo.mp4")
                              asyncio.sleep(5)
                            except:
                              os.remove("savevideo.mp4")
                              ctx.channel.purge(limit=1)
                        except:
                            pass
            if count == 10:
                return

    @commands.command(name="rand",
                      help="Sends a number random posts from subreddit")
    async def rand(self, ctx, subreddit: str, *, amount: int = None):
        pass
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
            return
        if not amount:
            amount = 5
        sub = await self.reddit.subreddit(subreddit)
        count = 0
        submission_list = [
            submission async for submission in sub.hot(limit=200)
        ]
        for count in range(0, amount):
            r = random.randint(0, 199)
            post = submission_list[r]
            url = post.url
            if url.startswith("https://i.redd.it"):
                await ctx.send(post.title)
                await ctx.send(post.url)
            elif url.startswith("https://v.redd.it"):
                async with ctx.typing():
                    if checkReddit(url, 60):
                        try:
                            downloadReddit(url)
                            renameReddit("savevideo.mp4")
                            try:
                              await ctx.send(
                                post.title,
                                file=discord.File(fp="savevideo.mp4"))
                              os.remove("savevideo.mp4")
                              asyncio.sleep(5)
                            except:
                              os.remove("savevideo.mp4")
                              ctx.channel.purge(limit=1)
                        except:
                            pass


def setup(client):
    client.add_cog(Commands(client))

