import discord
from discord.ext import commands
import random
import platform
import cogs._json


class For_Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("For_Owner Cogs has loaded")

    @commands.command(name="leave",help="Leaves the server")
    @commands.is_owner()
    async def leave(self, ctx, *, id_guild):
      guild = await self.client.fetch_guild(id_guild)
      await guild.leave()
      await ctx.send(f":ok_hand: Left guild: {guild.name}")

    @commands.command(name="logout",
                      help="Logs out of discord")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send("I'm logging out now.:wave: ")
        await self.client.logout()

    @commands.command(name="blacklist", help="Adds someone to blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

        if self.client.user == user:
            await ctx.send("You cannot blacklist me, idiot")
            return

        data = cogs._json.read_json("blacklist.json")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data,"blacklist.json")
        await ctx.send(f"Hey, I have blacklisted {user.mention} for you.")

    @commands.command(name="unblacklist",
                      help="Removes someone from blacklist")
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        data = cogs._json.read_json("blacklist.json")
        if not user.id in data["blacklistedUsers"]:
          await ctx.send(f"{user.mention} is not in blacklist")
          return
          
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data,"blacklist.json")
        await ctx.send(f"Hey, I have unblacklisted {user.mention} for you.")

    @commands.command(name="show_users",help="Shows all Blacklisted users")
    @commands.is_owner()
    async def show_users(self,ctx):
      data = cogs._json.read_json("blacklist.json")
      for id in data["blacklistedUsers"]:
        await ctx.send(f"<@{id}>")

  
def setup(client):
    client.add_cog(For_Owner(client))
