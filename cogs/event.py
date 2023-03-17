import discord
from discord.ext import commands
from data import *
import random
import datetime
import cogs._json


class Event(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.sniped_messages = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has loaded")

    @commands.Cog.listener()
    async def on_message_delete(self,message):
         self.client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(f"Welcome to {member.guild.name} my lad!\nInvite your friends https://discord.gg/mh9ynGua2Z")
        channel = discord.utils.get(member.guild.channels, name='general')
        embed = discord.Embed(description=f"Welcome to {member.guild.name}!",
                              color=random.choice(self.client.colors))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name='general')
        embed = discord.Embed(description='Goodbye from all of us..',
                              color=random.choice(self.client.colors))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        data = cogs._json.read_json("blacklist.json")
        if message.author == self.client.user:
            return

        if message.author.id in data["blacklistedUsers"]:
            return

        elif msg == "test":
          await message.channel.send("Test")

        elif msg in user_greet:
            await message.channel.send(random.choice(greet))

        elif msg == "bye" or msg == "goodbye" or msg == "good bye" or msg.startswith(
                "bye"):
            await message.channel.send(random.choice(depart))

        elif msg == "die" or msg == "mar":
            await message.channel.send(
                "Please do not kill me i have several families")

        else:
            if " lol " in msg or msg.startswith(
                    "lol ") or msg == "lol" or msg.endswith(" lol"):
                await message.channel.send("LoL")

            elif " lmao " in msg or msg.startswith(
                    "lmao "
            ) or msg == "lmao" or msg == "lmfao" or " lfmao " in msg or msg.startswith(
                    "lmfao ") or msg.endswith(" lmao") or msg.endswith(
                        " lmfao"):
                x = random.randint(0, 5)
                if x == 0:
                    await message.channel.send("hehe")
                elif x == 1:
                    await message.channel.send("LMAO")
                elif x == 2:
                    await message.channel.send("LMFAO")
                else:
                    await message.channel.send("Bruh")

            elif " waifu " in msg or msg.startswith(
                    "waifu ") or msg == "waifu" or msg.endswith(" waifu"):
                await message.channel.send("Touch some grass.")

            elif " bruh " in msg or msg.startswith(
                    "bruh ") or msg == "bruh" or msg.endswith(" bruh"):
                await message.channel.send("BRUHH")

            elif msg.startswith("wtf ") or msg.startswith(
                    "f "
            ) or msg.startswith("fuck ") or msg.startswith(
                    "fock "
            ) or msg.startswith(
                    "fack "
            ) or msg == "wtf" or msg == "f" or msg == "fuck" or msg == "fack" or msg == "fock":
                await message.channel.send(random.choice(comebacks))

            elif msg.startswith("imagine"):
                await message.channel.send(random.choice(imagine_words))

            elif msg.startswith("say it with me"):
                new_l = msg.split("e ")
                new_m = msg.split("e ")[1]
                for i in range(2, len(new_l)):
                    new_m = new_m + "e " + new_l[i]
                await message.channel.send(f"YEAH...{new_m}")

            elif msg.startswith("i wish"):
                await message.channel.send("Aukat me raho bsdk")

            elif msg.startswith("pagal") or msg.startswith("abe pagal"):
                await message.channel.send("Tu sab se bada chutiya he")

            for seg in bot_roast:
                if seg in msg:
                    await message.channel.send(
                        "Don't lump me in with your mom.")

def setup(client):
    client.add_cog(Event(client))
